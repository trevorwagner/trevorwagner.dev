---
title: "Collating Test Methods to Limit Trips to External Systems in Automated Tests"
publishDate: "2023-06-29T16:16:00-05:00"
coverPhoto: "https://static.trevorwagner.dev/images/sebastien-uwagwk2FywU-unsplash/1200x797.jpg"
thumbnail: "https://static.trevorwagner.dev/images/sebastien-uwagwk2FywU-unsplash/300x199.jpg"
draft: false

---

Very commonly I've seen series of automated tests that make separate, individual API calls to evaluate the HTTP response code and the response body returned by an endpoint. Or separate calls to an external CPU-intensive system. Or separate file system calls (to be fair I believe I've seen this one in tests I've written). Each test makes its own call to the external system and processes the results of that call within the system.  

This approach to test design seems to be pretty common, but I believe there is a better approach.  In this post I will expand on this approach, as well as what I believe the potential benefits and drawbacks of this approach are.

The pattern I see commonly generally makes the test methods that use it atomic. Here is an example (written in JavaScript, using Jasmine for test runner and assertions):

<pre><code class="language-javascript">
describe(`a GET call to the people/id endpoint`, () => {
   it(`returns HTTP 200`, async () => {
      const response = await axios({
         method: ‘get',
         url: ‘http://example.com/people/id/1',
      });

      expect(response.status).toEqual(200);
   });

   it(`returns a response with a JSON dictionary containing five keys` async () => {
      const response = await axios({
         method: ‘get',
         url: ‘http://example.com/people/id/1',
      })

      expect( () => { JSON.stringify(response.data) } ).not.toThrow();
      expect(Object.keys(response.data).length).toEqual(5)
   });
});
</code></pre>

...and so-on. Every test method runs its own axios call, which then waits for a response from the endpoint/ server in order to continue running tests.

It's nice, but it could be better. Consider this as an alternative:

<pre><code class="language-javascript">
describe(`a GET call to the people/id endpoint`, ()=>{
   let response;

   beforeAll(async ()=>{
         response = await axios({
           method: ‘get',
           url: ‘http://example.com/people/id/1'
         });
   });

   it(`returns HTTP 200`, ()=>{
      expect(response.status).toEqual(200);
   });

   it(`returns a JSON dictionary`, ()=>{
      expect(()=>{ JSON.stringify(response.data) }).not.toThrow();
   });

   it(`returns a JSON dictionary containing 5 keys`, ()=>{
      expect(Object.keys(response.data).length).toEqual(5);
   });

   it(`returns 'John Doe' as a value for the 'name' attribute`, ()=>{
      expect(response.data.name).toEqual('John Doe');
   }):
}):
</code></pre>

This is a pattern I've used successfully in a couple different programming languages (mainly JavaScript and Groovy). By collating test methods (at least, that's what I call it) in such a way that they all depend on a reduced number of calls for data (here: one), you reduce the number of operations you need to make in order to get the data you need to run each test. A little further below, I'll expand on why I believe it pays to use this pattern.

## When to Use this Pattern

I'd suggest using this pattern any time your tests require you to make a call to an external/ asynchronous system -- especially if you have multiple points of data you would like to validate in your response from that system. So if your test makes a call to an external system where some other processing needs to happen, then that external system needs to return a response, that might be a good opportunity to use this pattern.

Examples include:

- Making an API call.
- Making a call that interacts with the file system.
- Making a call to interact with databases (particularly databases that are not in-memory, likely also when potentially returning large data sets).
- Making a call to React to render components.

And to be clear here: I don't mean to use the term asynchronous in terms of the JavaScript event loop or in terms of the async/ await API.  I mean asynchronous more generally, in terms of [the sort of asynchronicity that can pose a challenge to test determinism](https://martinfowler.com/articles/nonDeterminism.html#AsynchronousBehavior).

Also to be clear (and I believe is relevant to the Martin Fowler link): the tests I collate all share a system state within the `describe()` statement; this keeps them isolated.  The shared setup sets system state and triggers the behavior under evaluation: the collated tests all evaluate the same system state independently.  Specifically within my example, I would expect `afterAll()` within the callback for the same describe statement the [axios](https://www.npmjs.com/package/axios) call is made to tear down system state in order not to pollute other tests.

Whether or not it seems obvious to external systems that present risk to your tests.  Generally you'd expect them to return the expected data; sometimes they bomb out for unexpected reasons (it can happen).  And any time you use them, you invest time and system resources in running them -- even if for a fraction of a second.

## Why I Use this Pattern

In essence, the second pattern makes fewer calls to `http://example.com/people/id/1` in order to retrieve data that it will evaluate later within assertion statements.  Nearly all of the benefits I will describe here trace back to this.

Because fewer calls are made, this pattern is more efficient: using this test design will pay dividends at volume. Let's say you have 30 endpoints that you test like this (4 test methods X 30 endpoints = 120 tests in runtime). Let's say it takes 400ms to execute an API call: with 60% reduction in HTTP requests executed, you can expect to reduce test runtime by 3 seconds. In my experience, most test suites that provide thorough coverage implement more than 120 tests.  

If you multiply whatever your savings across your suite is by the number of automated test runs you execute in a day, that's savings that ultimately adds up.

Because the second pattern makes fewer trips, I believe it also limits the number of opportunities for error in the external system that your test code interacts with.  For some reason or another, when we call external systems for data, things just don't line up and for some reason we don't get the response we expect.  Maybe it's a general performance bottleneck (and our response times out), maybe something happens somewhere else along the way.  Sometimes things just happen.

Not to mention the code in the second example is simpler, cleaner code. At least it seems that way to me: you make a call at the top, then below you provide a checklist of things you expect to evaluate within the result of that call. For me this aligns fairly well with [the way I typically plan testing](https://www.trevorwagner.dev/2023/06/24/how-i-write-test-plans-for-new-functionality/).  And in general, I believe the second pattern is easier to read than the first.

## Design Trade-Offs

There are two drawbacks I've been able to identify with a pattern like this.  The first relates to when the method making the API call (within the lifecycle hook) fails.  The second relates to when it doesn't. Both potentially limit coverage (arguably) within a given test run; in my experience, though, it doesn't seem like the risks presented by either outweigh the benefits.

The first drawback seems pretty obvious: the combined API call (within the lifecycle hook) presents a single point of failure to any tests that depend on it. When they fail, the matching library will report that response is undefined somehow. So although the API call is a single point of failure, it's possible to mitigate, and over time you're still enjoying all of the benefits of not making unnecessary API calls.

The second drawback is that if you are making these calls to the system under test, you lose additional coverage (at volume) that might have been provided by calls you have now designed your tests not to make. Let's say you were using the first example: with all of the API calls you make there you're essentially hammering the system under test with several requests for what is essentially the same information. The more you hammer the system under test, the more you exercise it, and the more opportunities you provide for something to potentially fail. To me this sounds a lot like endpoint profiling, which might be best performed somewhere other than system behavioral testing.

## Where You Can Use This Pattern

In essence the main idea is to use lifecycle hooks to make a call to an external system, store the result as a member of the class or method that would otherwise contain tests (i.e. in some scope outside of the test methods themselves), then run tests against the stored result.

There are degrees to which it seems like anybody should be able to use a pattern like the second one with nearly any test runner.  I could do this (to a certain degree) in JUnit 4 or JUnit 5.  With a specific glue code class design (where the response was stored on the class as both the step making the call and the assertion steps), I understand I should be able to do this with CucumberJVM (also with CucumberJS).  I've used this before in Spock; my tests were defined in Groovy.

In JavaScript I tend to nest `describe()` statements within other `describe()` statements.  So I get mileage out of drilling down from an outer/ high-level `describe()` block (where I do setup and teardown of system state), then doing the work of retrieving the data I'll be evaluating within the inner/ lower-level `describe()` block.

Also, in Spock I believe I recall pairing this somehow with table-driven testing.

## Conclusion

It pays to save trips. At one point I was asked (as a sort of ice-breaker question) when I get gas for my vehicle: do I go right away at a quarter of a tank, or do I wait for the low fuel indicator to display (i.e. wait until it's an emergency)? My answer here was that because I have several machines (lawn mowers, motorcycle, snowblower, chainsaw, etc.) in addition to my primary vehicle that use gas, I combine my trips to the gas station: I try to fill as much as I can up (both the tank and gas cans) in one trip.

The same way every trip to the gas station uses gas, every trip to an API endpoint, to the file system, or another external system uses resources and takes time. Using the pattern I've expanded on here has helped me limit the number of trips I make for data in order to be able to make several granular inspections of that data.  Like with any design decision, this approach presents drawbacks, but in my experience the drawbacks haven't outweighed the benefits. For me, it definitely beats crossing the desert every time I need some data to test.