---

title: "More than a Hot Take: Test Specifications Should Generally Not Determine for Themselves What They Intend to Evaluate"
publishDate: "2025-03-07T14:07:08-06:00"
coverPhoto: "gunnar-bengtsson-5t7vrCXrFMI-unsplash"
draft: false

---

It seems fairly commonplace that, when I evaluate tests in an existing codebase, I encounter test specifications with operational logic is defined in such a way that they (the specifications) determine for themselves what (if anything) they intend to evaluate within test runtime. Based on this determination, the specifications then execute assertions defined for any specific case logic that follows the determination. In some cases, which assertions are executed is a function of this determination. In others (or sometimes the same), how output gets evaluated within assertions is a function of another (or even sometimes the same) determination.

**Declarativeness** is a quality of automated tests with high ROI that does not seem to get mentioned often but which can have an impact on how test specifications that embrace it benefit from **integrity**, **operational independence**, and **readability**. Meanwhile, the more any test or test support code serves to circumnavigate an opportunity to declare by responding to state or status (and the more complex the circumnavigation), the less a test can potentially expect to enjoy any of these benefits.

Despite the benefits of declarativeness, there are three approaches to test design I've encountered in support of strategies to determine what should be evaluated within test runtime:

- Delegating this work to **a shared helper method that determines, based on an evaluation of _output_** produced during test runtime (possibly after transforming that output, as well) to determine which (if any) assertions should be executed (then executing them based on the determination).
- Delegating the work of executing all (or part) of a specification's operations to **a shared helper method that determines based on evaluation of _input_** provided to the test what (if anything) should be evaluated.
- During test runtime, evaluating the result of some asynchronous event (like the response of an API call or a call to the filesystem) and using **conditional logic that depends on the result of the evaluation to determine what to assert** or even whether or not to execute assertions at all.

Looking at strategies like these strictly from an operational- or code-design perspective, it seems relatively clear why somebody might make (and implement) design decisions like these for automated tests (I'll touch on this a little with the examples). In terms of test design, though, approaches like these present clear issues defining the inquiry a specification is expected to execute in service of and in terms of a specification serving as a source of clear signal related to the current functional state of work product that is usable to produce the data and feedback organizations rely on automated tests for to begin with.

I admit that I'm actually guilty of this (if not just potentially guilty -- mainly the second example) myself, usually when I write parameterized test specifications. And while on one hand it would be tempting to dismiss any of these examples as clear antipatterns, it seems like it might be more helpful to explore a little more closely the ways in which approaches like these to test design can be problematic.

This post will explore the negative design trade-offs of test code design choices that prioritize responsiveness over declarativeness. The conclusion will also provide some brief examples of where this distinction becomes more of a challenge to navigate and how one might go about navigating design decisions when it does (become more of a challenge).

## Reduced Test Integrity
In essence, each automated tests specification functions as a means of defining test runtime such that it produces clear signal reflective of the current functional state of work product. From the results test specifications produce in runtime, we collect data and feedback we can use to inform business intelligence related to functionality exhibited by the feature set being evaluated. The clarity of that data and/ or feedback depends on how well a test's design serves to produce signal that is usable as data, because it clearly reflects functional state.

An important quality of this ability to provide usable data and feedback is test integrity. It may be worth bearing in mind here that, at the same time every test specification works as code to define runtime, it also delivers value as a test. In essence, we understand what we do about how software behaves because we test, but we know more specifically because the tests we execute behave the way we expect them to. Tests with a high degree of integrity execute consistently, and they produce results that provide clear signal. It's due to both of these forms of integrity specifically that we can rely on the data and feedback a test specification produces during test runtime.

When a test determines for itself which (if any) assertion statements it will execute during runtime, it introduces additional complexity to the test that challenges the ability of the specification to run consistently or (although, possibly: and) produce data and feedback (by way of test results) that serve as clear signal reflective- or indicative of current functional state.

In the following Python sample (assuming `APIClient.do_POST()` returns a response that looks like what `http.client` returns out of the box), suppose the specification short-circuits the assertion if the server is unable to return either `200 OK` or a redirect:

```python
def test_returns_email_address_if_person_record_created_successfully():
  client = APIClient()

  response = client.do_POST(
    path="/people/new/",
    data={"first_name": "Joe", "last_name": "Person"}
  )

  if response.status < 400:
      body = response.read().decode("utf-8")
      try:
          result = json.loads(body)
          assert result["email_address"] == "joe.person@example.com"
      except ValueError:
          return

```
For any experts on `http.client` reading this, it might be worth assuming that `APIClient()` is a higher-level implementation that can be expected to handle HTTP redirects gracefully.

Conventionally, [test runners](/blog/?p=15) expect to post any of the following four results for a specification collected by the test runner during a test run:

- `pass`: when the specification executed, either _all of the assertions_ executed within the specification passed, or _no assertions were executed_.
- `fail`: when the specification executed, _one or more assertions_ that executed within the specification encountered a _mismatch_ between _expected-_ and _actual_ values designated for the comparison the assertion was tasked with.
- `error`: when it executed, the specification (or some extraneous functionality that the specification depends on, like a lifecycle hook or even test support code) encountered _an error or exception not related to an assertion_.
- `skip`: although the specification was collected, it was not executed because it was _specified not to be executed_ (often somewhere in test code).

For well-written specifications, each of these results provide clear _signal_ reflective of what happened within the test specification when it was executed (or even whether it was executed) during test runtime. The quality of the signal provided here is directly linked to the quality of the data and feedback that can be gathered from test results.

As a counterexample showing how this works, we generally don't parse through the logs of passed tests for clues as to what went as expected; we take it for granted that a result of `pass` reflects conformance to expectations. Unless we suspected an issue that warranted review, anything else would likely serve as a waste of resources.

As written, the specification provided in the example cannot be expected to execute consistently, and it cannot be expected to return a result that provides clear signal related to current functional state. In fact, this example specification presents three main codepaths, each leading to one of four distinct outcomes:

1. If `response.status` is greater than `400`, return a result of `pass`.
2. If `response.status` is less than `400` and `body` is not JSON that can be converted to a dictionary, return a result of `pass`.
3. If `response.status` is less than `400` and `body` can successfully be converted to a dictionary, run the assertion statement:
    - If `['email_address']` matches `'joe.person@example.com'`, return a result of `pass`.
    - Otherwise return a result of `fail`.

Although two results (`pass` and `fail`) can be expected here, exactly which operational outcome `pass` serves as signal for is not clear. Instead, it is _ambiguous_.

At the same time, though, it's worth considering what signal (by way of test results reported for a given run) a test designed like this could be expected to provide in any of the following scenarios:

- The request failed because `client` failed to login (or provide some credential like a CSRF token).
- The current login session for `client` has expired.
- The server was unable to authenticate `client` through a federated login source (like an LDAP server).
- `data` was somehow not processable by the server.
- A record for `Joe Person` was already persisted somehow in the database connected the API provides access to.
- There was an issue in the business logic between the API and the persistence layer.
- The path `/people/new/` was no longer made available (i.e. could not be found by the server in response to the request) through this API.

In each of these cases, how would a specification providing the codepaths listed above serve as a reliable source of data related to current functional state?

Whether a test passes or fails, the result produced by a well-written specification in runtime should somehow be _significant_. To depart a little from computer science and wade a little into how we study what is significant and why (more specifically [Semiotics](https://en.wikipedia.org/wiki/Semiotics)): whether a test fails, passes, or otherwise, the result should serve as [a sign](https://en.wikipedia.org/wiki/Sign_(semiotics)) for something recognizable to readers: it should be recognizable as representative- or indicative of (thereby providing data and feedback related to) some aspect of functional state.

A test that focuses on declarativeness should produce clear signal: it has successfully _designated_ each possible result as clear signal for an end state within the specification's operations that (regardless of what the result actually is) can easily be interpreted by reviewers. Alternatively, a specification that responds to state or status produced during test runtime (specifically as noted here: one that presents several codepaths that lead to results that do not clearly indicate- or reflect how functional state is evaluated within the test) will likely produce signal that is ambiguous in a way that is unhelpful as a source of data and/ or feedback.

## Reduced Operational Independence
Although it's often cited that a good test is an **atomic** test, what _atomic_ actually refers to appears to be open somewhat to interpretation. Most often, _atomic_ is used to describe _a test that does not rely on state or status (or other conditions) established within- or maintained by other tests in order to be a valid test_. Some might prefer to describe either of these examples as _self-contained_. It's likely a better fit than [common definitions of atomic](https://en.wiktionary.org/wiki/atomic), which reflect use of _atom_ (at least, [traditionally](https://en.wikipedia.org/wiki/Nuclear_fission#Discovery_of_nuclear_fission)) to describe the smallest indivisible unit of matter.

Again: test specifications aren't just code defining operations (they also deliver value as a test), but when designing test code it pays to be intentional about how both the design of the code and the definition of the test (through test code) work together. A test that produces clear signal should declare for itself how exactly it will undertake the operations necessary to return the expected data and feedback expected of it (by executing the inquiry it is responsible for).

By contrast, test code design that delegates the determination of what gets evaluated (and why) to a helper method also outsources declaration of how the test itself should be executed (thereby provide signal). What gets evaluated (and how) now depends on something completely outside of the control of the specifications that depend on it. That may be problematic now; it could also be problematic over time. And the definition of how this determination is executed is subject to change.

When test specifications rely on shared code to determine what gets evaluated (and how), they encounter two problems related to code structure that pose a challenge to test integrity: one is **operational dependency** on functionality outside of the test's control, and the other is formal **code coupling**.

Consider the following example:

```javascript
const executeRelevantAssertions(v) {
  const result = v / 2
  if (v % 2 == 0) {
    assert(result % 1).toEqual(0)
  } else {
    assert(result % 1).toNotEqual(0)
  }
}

describe(`functionality`, () => {
  it(`works for one case`, () => {
    // perform some test operations, i.e. `arrange` and `act`
    executeRelevantAssertions(1)
  })
  it(`works for a second case`, () => {
    // perform some test operations, i.e. `arrange` and `act`
    executeRelevantAssertions(2)
  })
  it(`works for a third case`, () => {
    // perform some test operations, i.e. `arrange` and `act`
    executeRelevantAssertions(3)
  })
})
```

As implemented, each of the `it` methods provided above is operationally dependent on `executeRelevantAssertions()`: none can execute any of the assertions (which, for illustration, follow some unnecessarily complex math to determine whether the value assigned to `v` is even or odd, then assert based on the determination that `v / 2` is a whole number) as specified without executing the helper method. As tests, then, none of them (as implemented) can carry out the inquiry they are required to without referring to the helper method that defines operations related to selecting and executing the expected assertion statements.

And to be clear, `executeRelevantAssertions()` does not key off of state or status produced within test runtime as implemented currently; this example was implmeented the way it was for simplicity. It would be very easy, though, to produce state or status in test runtime and pass that as an argument to `executeRelevantAssertions()`, which would determine what (if anything) whould be evaluated and evaluate based on the determination.

Tests designed like this experience the same problems as a source of signal: much like with the example in the last section, the signal each specification provides during runtime is now a function of whatever `executeRelevantAssertions()` does, however it is currently implemented.

With all of this in mind, none of the `it` methods/ specifications can be argued is atomic. Or even self-contained.

As an alternative, one might consider renaming `executeRelevantAssertions()` to `numberIsEven()` and modifying its definition to return `true` in the first case (and `false` in the second; the example provided in next section actually shows what this would look like) instead of executing the specified assertions. With these changes, each specification could declare its own assertions individually (i.e. `expect(numberIsEven(2)).to.be.true`) based on the value returned by `numberIsEven()`. With this alternative approach, test operations would virtually remain the same, but test design would uncouple the code and remove operational dependence of the test from `executeRelevantAssertions()`. With these changes, the tests would actually be atomic (and would serve as clearer sources of signal), because they would now be more declarative.

As an alternative to the example provided above, though, I've seen whole specifications that accept a limited set of arguments and call an external helper method (sometimes the helper method is the direct callback of the `it` method) that does all of the work of defining and running the test, including whichever assertion statements are appropriate depending on the case the helper method is expected to respond to in test runtime.

Because the code defining these tests (as implemented currently) is coupled to `executeRelevantAssertions()`, any change to `executeRelevantAssertions()` runs the risk of changing the definition of any test specifications that depend on it to determine what gets evaluated (and why). There is currently no way of validating that the specifications continue to execute the same as before (short of confirming that `executeRelevantAssertions()` throws the expected assertion errors for the expected cases, which would likely work at small scale but would likely present issues in more complex examples), even if the same tests return the same results after the change as before.

Within the alternative (see below), not only do the tests avoid this problem; they also provide an opportunity to make the helper method testable on its own. And although it's clear here that the output of `numberIsEven()` is what the tests are asserting (as a means of executing inquiries into functional state), test design like this would lay the groundwork for a different helper method (in place of `numberIsEven()`) to be tested independently, to verify that, if it is modified somehow, it continues to lend support to test specifications as expected.

## Reduced Test Readability
Activities related to reading automated test code can get expensive for organizations that depend on the tests the code defines. Wether the activity in question seeks to understand how a test defines its operations, to organize or disposition tests, or to troubleshoot or debug tests that have failed (whether locally or in CI), any activity that depends on automated tests being readable runs the risk of being some of the most expensive an organization will invest in for affected tests. The more tests promote simple and wide-reaching readability (sort of like writing texts at a fifth-grade reading level to promote accessibility), the more they can proactively reduce the impact of activities that depend on readability.

For test code, this goes beyond interpreting test results (which, as described above, challenges to test declarativeness can increase the complexity of); it also goes for how the implementation of any specification seeks to _define automated test operations_, how it serves to _define how a test executes in service of an inquiry_, and how it seeks to _produce clear signal through its results_. All of these things are effectively encoded within the definition of any test specification, and the ability of any test specification to make any of these encodings apparent will increase the readability of the specification.

Test design that responds to state or status produced within runtime can have the effect of **increasing code opacity** as well as **proposing an esoteric system** for test specifications that depend on it by making the code that defines test operations (and any relationship between operations and the inquiry the specification executes in service of) a challenge to follow and likely also difficult to map out.

As an alternative to the JavaScript example in the last section, consider the following:

```javascript
function numberIsEven(v) {
  return (v % 2 === 0)
}

describe(`functionality`, () => {
  it(`works for one case`, () => {
    // perform some test operations, i.e. `arrange` and `act`
    const result = numberIsEven(1)
    expect(result).to.be.false
  })
  it(`works for a second case`, () => {
    // perform some test operations, i.e. `arrange` and `act`
    const result = numberIsEven(2)
    expect(result).to.be.true
  })
  it(`works for a third case`, () => {
    // perform some test operations, i.e. `arrange` and `act`
    const result = numberIsEven(3)
    expect(result).to.be.false
  })
})
```

If we wanted to simplify more, we could potentially convert the individual specifications to a single [parameterized test, at which point we could correlate inputs and expected results (within something like an array of JavaScript objects and let a shared test specification iterate through the test cases row by row](/blog/?p=19).

The revisions provided in the example here are generally readable as-is, though, too. By contrast, the original example (from the previous section) assumes that any reader understands (clearly) what the logic defined within `executeRelevantAssertions()` relates to. It clearly does some operational work as test code, but how that work relates to the inquiry any specific test specification is responsible for may not be clear without additional analysis (or assistance -- of which, for reference, either is resource-intensive), which could become problematic at scale (i.e. with many tests). The same is true for the signal any consuming test specification is tasked with producing. This presents (along with code fragmentation and additional cyclomatic complexity) _code opacity_ that any reader would need to cut through (if they have not already) in order to successfully perform any activity that depends on code readability.

As is, then, the example from the previous section is an _esoteric system_ (sometimes alternatively described as an _expert system_): somewhere between test operations, the inquiry, and signal, the test only makes sense to the initiated. In more complex cases, where the work helper methods like `executeRelevantAssertions()` responds not just to state produced in runtime but also to the implementation of the system under test, can (like any helper methods) serve as a system where the initiated require not only intimate knowledge of how test code defined (and why) but also production code.

## Conclusion
Ultimately, automated test specifications are expected to deliver value in the form of data and feedback produced upon evaluation of the system under test: with automated tests specifically, that data and feedback reflects how the specification completed execution during test runtime. In essence, then, the way a test executes in runtime serves as signal related to functional state. Because the integrity of this signal plays an important role in its validity and actionability, automated tests designed to make the relationship between all of the following clear are generally more valuable than those that only make some (if any) of them clear:

- How the specification **defines test runtime**.
- **What the inquiry is** that a test specification executes in service of, and how specifically the operations defined for a test specification execute in service of that inquiry.
- How any **result** a specification arrives at (or any end state the test has been designed to reach) during runtime **serves as signal** is usable as a source of data and/ or feedback.

Generally, the less declaratively an automated test specification defines the way in which it executes on behalf of an inquiry, the less integrity the test runs with, and the less value the test presents as a source of clear, accessible, actionable information. Specifically, when specifications are designed and implemented in such a way that they determine independently what should happen based on state or status produced within the test, they run the risk of trading the value of clear test results (i.e. data and feedback), and the signal they produce for any sense of convenience responsiveness can be expected to provide.

I am actually (somewhat) guilty this myself sometimes. And like any design decision, the principle is usually easier discuss than the actual implementation. Even within posts I've made to this blog I provide examples of tests that respond to state or status. Take for example:

- In [this post, which provides a design overview of a framework (and suite of tests) I wrote using Cucumber-JVM](/blog/posts/code-walkthrough-simple-framework-running-ui-tests-with-cucumber-jvm-sprinboottest-and-selenium/), I discuss how I make use of a step definition that uses the substring `should` or `should not` as a parameter to define the polarity (in essence, `true` or `false`) of an assertion statement for the resulting step definition.
- In the introduction to [this post, which explores the benefits of embracing DRY through parameterized test specifications](/blog/posts/test-parameterization-exploring-reusable-test-design-and-the-benefits-of-making-automated-test-code-dry/), I provide a code sample where the specification uses a value passed in through the test case (specifically the value specified for `p`) as the expected result in the assertion statement.
- In [this post, which explores the benefits of throwing errors and exceptions in response to unexpected state or status in tests](/blog/posts/making-the-most-of-throwing-errors/), I suggest using a series of checks to enforce an expected set of conditions within an automated test. If a test encounters state or status (produced within test runtime) that does not conform to expectations, throw an error that flags the test as non-conforming (potentially also stopping test execution).

Hopefully it's clear how I've approached each example as declaratively as possible. With the post regarding Cucumber-JVM, step/ feature text (defining the test itself) declares _should_ or _should not_ (and unit tests are used to confirm fidelity to user expectations). With the post dealing with parameterized teswt specifications, care is taken to make the complexity of modification of a value minimal, and to respond specifically to values defined by the user (as opposed to values produced elsewhere within test runtime); I do the same thing if I encounter [similar sorts of design choices with nested test specifications](/blog/posts/collating-test-methods-to-limit-trips-to-external-systems-in-automated-tests/). And within the post regarding proactively throwing errors, the point here is to return a status of `error` if state or status does not meet expectations set explicitly within the test's definition.

Again, I believe a helpful rule of thumb here relates effective test design to its _declarativeness_ as a means of supporting test _integrity_. Anything that _responds_ to state or status that is produced within test runtime potentially opens itself to the sorts of limited integrity, limited atomicity, and readability issues outlined in the main sections of this post. The more complex either the response or the relationship between behaviors exhibited in test runtime and the point where those behaviors are declared, the greater any such limitation is likely to be.