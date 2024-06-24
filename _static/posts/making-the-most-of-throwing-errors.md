---
title: "Making the Most of Throwing Errors: Exploring Why \"Fail\" Could be One of the Most Valuable Things Automated Test Code Can Do"
publishDate: "2023-10-26T16:32:00-05:00"
coverPhoto: "https://static.trevorwagner.dev/images/alek-kalinowski-9HsRmdogZsU-unsplash/1200x800.jpg"
thumbnail: "https://static.trevorwagner.dev/images/alek-kalinowski-9HsRmdogZsU-unsplash/300x200.jpg"
draft: false

---

When writing tests, it can be easy to focus on the assertion statement as though it's the goal line and assume that the most important thing is to avoid anything that might stop the test from reaching the goal. After all, if the assertion statement is where the test confirms that the actual result returned by the system under test matches the expected result, that's proof that the behavior under evaluation within the test conforms to expectations.

With this understanding, the general strategy becomes keep the test specification marching runtime down the field toward the goal.

When I coach other engineers as they write automated test code, I tend to encourage them throw an error (also the appropriate exception in JVM-based test runtimes; going forward we'll just call it an error to keep things simple) if in a test if they encounter a situation where nonconforming state could challenge the integrity of the test. Maybe state does not conform because of an issue somewhere in test code. Maybe the issue lies with an external system (like an API, a filesystem, or a database) that did not respond as expected. Whatever the reason, the data that will ultimately reach the goal line (that is the assertion statement) will not look the way you expected it to for some reason or another. For situations where this might happen, throw an error within the test specification, throw in a step, throw in setup code, throw in a lifecycle hook, throw wherever makes the most sense. My advice is to be proactive about spiking a test, sort of like a quarterback in American football spike the ball in order to end a play (normally at the beginning of the play) in a manner that stops the game clock at the cost of a down.

It's also a lot like the referee throwing a flag on a play. We'll explore this a little in the conclusion.

I actually tend to say it with the timbre of a football coach encouraging players to do something strategically beneficial even if it might not immediately seem like common sense:

_Don't be afraid to spike a test if it's not doing what you want it to._

In JavaScript, for example, code to throw an error can look as simple as this:

<pre><code class="language-javascript">
if (instance.fieldValue !== 1) {
   throw Error(`Expected fieldValue to be 1, but was ${instance.fieldValue}.`)

}
</code></pre>

At a strictly technical level, failing a test proactively conventionally results in three things:

- Test runtime for the current test specification stops.
- The current test run will complete with a status of failure (which will cause, for example, any build/ task that started the test run in CI will complete with a status of failure).
- The error message provides an opportunity to return timely information (including an error message and a stack trace) related to the point in test code where the failure occurred.

These three things together amount to 90% of the reason why within the test data management solution I built to facilitate running UI tests with a mock backend, I wrote the code to throw an error in several situations where requests showed the potential to produce or retrieve duplicate test data, and I wrote test code to confirm that errors were thrown as expected. This defensive coding strategy was effective in practice, and I believe the reasoning behind the strategy is sound. I thought it might be valuable to try to share a little of both.

And to be clear: assertion statements aren't the only point in test code for which it helps to be defensive about state. Maybe we want to make an API call (or read from a database) with a specific set of credentials. Maybe we expect a certain number of elements to have been added to a queue or stack. Maybe we expect a specific element to be present on a Web page. The same way state can result from any of these things, state can (depending on how our code is written) potentially affect our ability to accomplish any of these things successfully within an automated test. For simplicity, though, I will focus within this post on assertion statements as a point in test code most likely affected by nonconforming state.

Arguably, reporting on a failure can also be accomplished within logs. In combination with the first two, though, failing a nonconforming test deliberately can be a powerful tool that can help prevent (if not just limit) waste.

This post will outline why I believe this is.

## Different Reasons for Failure

Before we get too far, it might be worthwhile to return to the well-worn ground of differentiating the two types of issues that automated tests can encounter that cause them not to pass:

- **Test Failures** happen in code due to an assertion error: when the actual result does not match the expected result (more below), the assertion statement tasked with comparing the two throws an assertion error of some sort. This fails the test.

- **Test Errors** happen in code due to an error being thrown of any type other than an assertion error. Such an error can be thrown anywhere within runtime for a test specification (test method, Gherkin scenario).

When debugging non-passing tests, this distinction can actually be helpful: in a test where the expected behavior is clearly defined, a **test failure** generally indicates an issue in the system under test (because the comparison in the assertion statement failed), and a **test error** could reflect a failure in the system under test, the testing system (i.e. the test framework, test specifications, test support code, etc.), or anything (operating systems, networking, external systems, etc.) expected to support the former.

At a high level within this post (as well as within the title), I will refer to both as test failures. The frame of reference I'm working from is that, when we describe a test run as having "failed in CI", it generally doesn't help to get granular about whether tests failed or whether they encountered an error. Where it helps, though, to explore either issue type separate from the other I will differentiate the two.

Also a quick note that with my thesis I don't mean to attempt to litigate whether it potentially makes more sense to use an assertion statement (which tends to be more concise in code than checking state and throwing an error) when performing a check in a test. My (strong) preference is for throwing an error; hopefully given the time I've dedicated to the breakdown in this section it's clear what informs that preference.

## Errors Halt Test Runtime

Once an automated test specification (test method, Gherkin scenario, etc.) throws an error (general error, assertion error, or otherwise), any test runner I've worked with with will stop running it. Stopping the test from running prevents test runtime from proceeding any further (including reaching the assertion statement) with state that is out of conformance (i.e. test state, system state, or otherwise doesn't look the way you expect it to) in a manner that challenges the integrity of the test.

For a moment, imagine two scenarios:

- **Despite the fact that test runtime reaches the assertion statement, something went wrong very early on** that results in state not conforming to expectations. Despite this, the test continued to run, and although no errors fired earlier in the test, the actual result now differs from the expected result when the assertion statement is executed. The test fails in response to assertion error (at which point it's up to the engineer to track down the point where state started not to conform that led to the assertion error).
- The same test encountered the same issue in state early on. **Because logic within the test specification (or test support code) caught nonconforming state early, the test now fails at the point of detection.** The test stops running, and the error (with error message and stack trace) are printed to test results.

The second scenario is referred to in some circles as [failing fast](https://testsigma.com/blog/test-automation-achieve-fail-fast-fail-often/). As I understand it the term is somewhat unrecognized when discussing test design; I personally believe it deserves greater visibility.

And to be clear, it's not just an error thrown directly within a test specification or step method that stops a test from running. Throwing an error within a **test lifecycle hook** (something like `before()` or `beforeAll()` in the main three JavaScript runners, JUnit's `@BeforeEach`, Cucumber's `beforeScenario()`, etc.), within any test runner I can recall having used will halt execution of both the lifecycle hook as well as the test specification/ step expected to follow it. So if a `before()` hook fails, the test specification it provides setup for will (again: in any test runner I'm familiar with) not run.

To take this even further: the error doesn't need to be thrown directly within test specification/ step/ hook code. As anybody who writes- and debugs tests will likely be familiar with, errors and exceptions thrown within **test support code** (either external libraries or custom-built code) also typically serve to halt test/ lifecycle hook runtime.

This convention can benefit us in two ways: it helps limit the amount of unnecessary test code that needs to run (after having encountered an error), and by reducing the amount of test code that runs, it reduces the amount of code we potentially need to look through to figure out what led to the error in the first place. In the next subsections, we'll examine each of these benefits a little more closely.

### It Generally Helps to Prevents Waste

Test code that stops running limits use of resources by the stopped test specification in three ways (maybe some in combination):

- The test stops occupying **system resources** (i.e. you no longer need things like CPUs, RAM, and network bandwidth to run it).
- The test no longer requires **time to run** (i.e. no system cycles in CI, potentially blocking other tasks).
- Nobody needs to wait for the test to finish running (in addition to the test running, there's no **operations time wasted on any engineers waiting for test results**, blocked by a build that needs to pass, etc.).

The sooner you can fail fast, the more it stands to reason you will save on at least two of these things (again maybe also the third). If you're running tests against several different environments (like a test run executed cross-browser), multiply savings by the number of variations for which the test can be expected to fail fast reliably. With a hook that runs setups for all specifications in a test class (think JUnit or Spock), a `describe()` block (think jasmine/ mocha/ jest), or a fixture (think pytest or behave), calculate the savings in terms of the sum of all tests that were deferred in response to the `before()` hook failing.

This is also my one argument against only logging (otherwise I have nothing against it and believe logging is generally helpful elsewhere) as an alternative: if all you do is log, then the test continues to run when likely you don't need it to. Failing fast can help prevent waste in a way that logging on its own does not.

### It Reduces the Haystack when Searching a The Root Cause of the Failure

Because an error of some sort limits the amount of test code that gets run (within a specification, lifecycle hook, or otherwise), it also limits how much code defining the failing test/ lifecycle hook needs to be traced through to find the root cause of the failure. If there was a failure and only part of the code ran, then the failure must have been related to the subset of the code that actually ran.

If all test code runs (and reaches the assertion statement) with nonconforming state, then the search field to locate the potential issue includes:

- All of the **test code** that was run until the point that an issue was detected.
- Any **log output** that was (potentially) saved until the point that an issue was detected.

If the test failed at a certain point in code, then the issue must have occurred before the point of the failure. Failing sooner reduces (in essence) the amount of test code and log output that potentially needs to be evaluated in order to isolate a potential root cause.

## Failure Provides an Opportunity to Return Diagnostic Information

At the same time errors can be helpful where they stop test runtime, errors can also be helpful as they execute: namely, where error messages provide two things that can hopefully help us pinpoint quickly what the nature of the issue is and where the issue occurred that contributed to a test failing:

- An error message.
- A stack trace.

One of the things that experience shows me tests can do to help make life easier for software engineers (in production, SDETs, or otherwise) is to provide enough information not to need to trace through test code in order to figure out either where the issue happened or what the nature of the issue was. Wherever I see an uncomplicated choice between cordoning off an afternoon (or, worse: evening) to debug test code and writing test code to tell me (proactively) what happened and where, I'll gravitate toward the latter.

In the subsections below we'll examine briefly why each of these is helpful (keeping in mind that the value is in conjunction with failing fast/ stopping the test, as outlined in the last section).

### Error Messages Can Help Describe the Nature of the Issue in Helpful Detail

Error messages provide an opportunity to let the test code (or the test support code) tell you what was happening when the error occurred. This goes beyond showing a sort of limited message that generally fits cleanly onto the sort of [variable-message sign](https://en.wikipedia.org/wiki/Variable-message_sign) you might find on the freeway: you can actually provide useful diagnostic information within your error message that (hopefully) limits the need to dig into code later. This, in my experience, also seems to help limit waste.

When I wrote [the test data management system I used to perform UI testing with a mock back end](/blog/posts/design-overview-in-memory-generic-test-data-managment-in-javascript-using-lokijs/), it was very important that tests fail fast if a situation was encountered that might cause ambiguity in test data. For example, if I wanted to retrieve one (and only one) record with the repository's retrieve(query) function, then I could expect that returning zero matches was a problem (I expected a record to be there but it wasn't) and returning more than one match (at which point for a query expecting a single match it's ambiguous which record the user meant to retrieve) was also a problem. I handle these both of these potential issues while also returning the one match I'm actually expecting with code like this:

<pre><code class="language-javascript">
if(matches.length > 1) {
  throw Error(`Expected to find only one record matching the query ${JSON.stringify(query)}, but found ${matches.length}: \n${JSON.stringify(matches.length)}`);
}

if(matches.length === 0) {
  throw Error(`Expected to find a record matching the query ${JSON.stringify(query)}, but found none.`);
}

return matches[0];
</code></pre>

If neither condition is true, the snippet returns the first match; if either condition is true, execution stops after the error associated with that condition (with corresponding error message) is thrown.

Within the error messages in this code snippet I do the following:

- Note what the expected state was (one and only one matching record).
- Note what the current state was instead of the expectation.
- Use current state (namely the count of matching records found within he repository) to provide a little more clarity on the summary.

Print (via `JSON.stringify()`) the offending state data to string where applicable.

If what I expect from current state is that there is one match, there is no need to continue if current state does not match expectations. At the same time, though, if there's anything I can extract from the failure in order to describe clearly what that nonconformance was (namely what I expected and how actual state deviated), then the failure is produces value beyond simply halting test/ lifecycle hook runtime.

### Stack Traces Help to Pinpoint (Maybe Also Provide Context) Where in Code the Problem Occurred

If an error was thrown within test runtime, any test runner I am familiar with will also provide a stack trace showing where in code the issue occurred, in addition to the call stack leading to the point where that code was executed.

In any programming language I've written tests within (Java, JavaScript, Python, and Groovy), the stack trace is printed (for free: no need to query for it in order to print it) whenever I throw an error.

Getting a stack trace is good if the error was thrown within the test specification itself; it's even better if it happened within test support code. If an error was thrown in a helper method or something like a factory class somewhere that was called within the test specification, then the stack trace will lead from that point in test support code to the point within the test specification where calls to test support code originated.

### Checks that Produce Errors can Serve as Passed Checkpoints

If your test incorporates several checkpoints and a test passes several checkpoints before failing at another, that might also provide insight into where to start searching for the root cause of at test failure.

Let's say that for some reason you have a particularly long test specification (or for some reason use a lot of support code within your test) where you needed to check a few times before you get to the assertion. Any point where a check actually passed can also be helpful to narrow down where the issue might have occurred. Let's say state in a test I wrote passed three checks, but the fourth one failed. If I'm checking the right things earlier in my test code, then somewhere between the third check and the fourth is likely a good place to start looking. I should also generally be able to take it for granted that, if state passed each of the three checks, that the list of possible root causes should be limited to the subset of possibilities that would have passed the first three checks.

## Conclusion

At the same time strategy is of the essence in American football, it's equally as important to maintain the integrity of the game. In American football, whether it's pass interference, encroachment, false start, holding, intentional grounding, illegal formation, too many men on the field, or even "[giving him the business](https://www.youtube.com/watch?v=x39z7Wjhj88&t=14s)," there are several behaviors that can lead to penalties being assessed that stop (or in some cases increase) progress toward the goal line. What those of us watching in the stands and at home expect from all the action, effort, and strategy is a clear victory from a good, clean game.

The same as with manual tests, what we expect from an automated test is that test execution maintains the integrity of the test as it exercises the system under test. We expect the environment not to change, we expect tests to be run in a manner that is predictable, and in general we expect the test to be able to produce the same result every time unless something changes within the system under test. If one of these things is not possible we should know right away (and ideally with some feedback as to why). Beyond this, the reasons listed above hopefully provide more concrete reasoning as to why I suggest throwing errors to fail fast and why I do so in test code I'm responsible for.

So don't be afraid to spike a test (or throw a flag as though you were the ref, for what it's worth) your test is not doing what you expect it to. In my experience, it's a great defensive coding strategy that helps to tighten the feedback loop for failing/ erroring tests (especially in situations where external systems are interacted with, where test support code or the system under test is complex, or anywhere that the integrity of state might pose a risk to the integrity of a test) while at the same saving resources (by stopping failing tests early). It could actually end up being valuable to making sure that the tests run the way you expect them to and that if you get an assertion error, it's the result of a good test instead of something you weren't prepared for.