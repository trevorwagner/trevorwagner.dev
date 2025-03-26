---

title: "Understanding Test Automation Frameworks: What is an Assertion Library?"
publishDate: "2025-03-24T15:45:14-05:00"
coverPhoto: "trevor-wagner/bike/reflect"
draft: false

---

Some of the most important work performed by an automated tests specification takes place within an **assertion statement**. At the most basic level, an assertion statement serves to define a comparison to confirm (when executed during test runtime) that output retrieved from the system under test (often referred to the _actual output_ or _actual result_) matches a set of conditions specified within the definition of the assertion statement. If there is a mismatch, the assertion statement generally emits some sort of error that results in the test runner reporting a result status of `fail` for the specification.

When used well, an assertion statement can provide all of the following benefits within the specification's composition by defining what gets evaluated and how:

1. It defines a **clear objective** for the inquiry that the specification executes in service of.
2. It provides **clear constraints** (by way of criteria for success) for test runtime and as well as **clear reporting** when a behavior exhibited by the system under test overshoots those constraints.
3. It provides a **clear focal point** to organize test composition around. Much like the role a topic sentence plays within a paragraph, assertion statements provide a description of the topic (by way the objective for inquiry) for the specification.

Beyond supporting good composition for an automated test, assertion statements play a key role in helping test specifications produce **signal** (by way of test results) that is vital to informing the data and feedback that automated tests are responsible for. In general, the clearer the signal is that a test specification produces when it is executed, the easier (also readable as: _more efficient_) it should be to gather data and feedback from test results (whatever the result was) in a manner that limits the need for in-depth investigation. When an assertion statement is used correctly, this signal is usable regardless of whether any specifications they execute within produce a result status of `pass` or `fail`.

Assertion statements are designed and executed using an **assertion library**. Much the same way that a test runner provides an API that supports defining test specifications that will be executed as part of a test run, assertion libraries each provide an API that make it possible to define three things clearly:

1. **How test code should execute a comparison** between actual output and any expectations (defined within the assertion statement).
2. **What the criteria are for both a comparison mismatch** (i.e. for the actual output _not to match_ the expected output) as well as a **comparison match**.
3. **Which output (or feedback) should be produced** in case of a comparison mismatch.

At the same time a test runner is an essential part of any test automation framework, then, so is an assertion library. If test runners provide (among other things) a form of locomotion for test runs (one after the other -- sort of like links in a chain on a bicycle), and assertion libraries help make it clear what assertion statements are attached to, sort of like a bicycle's reflector.

In general, there are two types of assertion libraries:

- **Standalone assertion libraries:** assertion libraries whose primary focus is to support creating and executing assertion statements, reporting on failures, and making it possible to create custom assertion statements. [Chai](https://www.chaijs.com/) and [Hamcrest](https://hamcrest.org/) are good examples of this: assertions is all they do.
- **Integrated assertion libraries:** that is, assertion libraries that serve as part of another library such as a test runner (like with [Jasmine](https://jasmine.github.io/api/edge/global.html#expect) or [JUnit](https://junit.org/junit5/docs/5.0.1/api/org/junit/jupiter/api/Assertions.html)), part of a test support library (like [Cypress](https://docs.cypress.io/app/references/assertions) or [the core Playwright library](https://playwright.dev/docs/test-assertions)), or which are supplied by the language/ runtime environment itself (as is the case with [Python](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement) and [Node](https://nodejs.org/api/assert.html)).

Whether the library in question is integrated or standalone, the focus of this post will be to examine the ways in which an assertion library delivers support for the definition, execution, and implementation (by defining custom matchers that extend the library) of assertion statements. 

By doing so, it will also attempt to _reflect_ (a little) on how assertion libraries serve as an indispensable part of any test automation framework.

## Assertion Libraries Provide APIs to Define Assertion Statements
A functional assertion statement is distinct from either of the two following types of statements:

1. A statement that evaluates to `false` like `True == False` in Python or `true === false` in JavaScript.
2. Throwing a custom error (like `ValueError` in Python or `Error` in JavaScript).

Generally speaking, neither of these types of statements is appropriate to define a comparison that can be expected to produce clear signal when executed (as part of a specification) during test runtime. When executed within many common test runners (to be clear, any runners I have attempted this with), the first type of statement will _not_ cause a test specification to fail: specifications that execute a statement that evaluates to `false` generally report a result status of `pass`. The second statement will cause the a test specification not to pass in runtime, but the test will report a result status of `error` (not `fail`). 

There will be more detail on test result status the next section, but for now this distinction worth noting on its own.

It helps to envision an assertion statement (much like what's outlined in list provided at the beginning of the introduction to this post) as an _opportunity to fail_. A test will fail (and provide usable signal) if and only if the conditions specified within an assertion statement to cause a failure are met. 

It's the terms of the comparison an assertion statement (within its definition) has been configured to execute that define these conditions. The more specific and definite this comparison is, the more likely a behavior is to trigger a failure if it meets the expected conditions.

The more clearly and accurately an assertion statement is defined, then, the more useful the opportunity to fail (or pass, as appropriate) the assertion is as a means of producing clear signal.

The **APIs that assertion libraries make available** to configure assertion statements as opportunities to fail **help make the terms that separate a passing result from a failing result** as **clear** as possible. Some assertion libraries (like [Chai](https://www.chaijs.com/) for JavaScript or [Hamcrest](https://hamcrest.org/) for -- basically a lot of programming languages, but which started as a Java project) support use of a custom syntax to make these terms read (and compose) as fluidly (lexically) as possible.

A Chai assertion against an HTTP response code could look like this:

```javascript
expect(response.status).to.equal(200)
```

Meanwhile, a Hamcrest assertion against something similar in Java could look like this:

```java
assertThat(response.status, equalTo(200));
```

Others, like Python's built-in `assert` keyword, expose a single keyword and expect that most any statement that follows it evaluates to `true` (otherwise throw `AssertionError`). To evaluate `response.status` in Python, consider this example:

```python
assert response.status == 200
```

In another example, though, verifying that an exception fired or did not fire when `myFunction` was run in Python ([here, for example, as documented for Pytest](https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions)) can require a little more custom wiring on the part of the developer than the following example does making use of built-in functionality provided by Chai:

```javascript
expect(() => { myFunction() }).not.to.throw()
```

## Assertion Libraries Facilitate Returning Clear Feedback from Test Runtime
One of the most important qualities of a well-written test specification is the ability to provide clear signal upon execution. Once it has executed, either a test will pass or it will fail. That is, unless it runs into some sort of issue along the way (which is out of scope for this post).

Once a test specification is collected by a test runner (i.e. identified by the test runner as a match for search parameters to locate tests that were specified when it was originally executed/ invoked), the test runner will (conventionally) report one of four distinct result statuses:

- `pass`: when the specification executed, either _all of the assertions_ executed within the specification passed, or _no assertions were executed_.
- `fail`: when the specification executed, _one or more assertions_ that executed within the specification encountered a _mismatch_ between _expected-_ and _actual_ values designated for the comparison the assertion was tasked with.
- `error`: when it executed, the specification (or some extraneous functionality that the specification depends on, like a lifecycle hook or even test support code) encountered _an error or exception not related to an assertion_.
- `skip`: although the specification was collected, it was not executed because it was _specified not to be executed_ (often somewhere in test code).

Generally, if a specification reports any result status other than `pass` upon completion, it helps to be able to quickly distinguish a failure from any other type of error. 

Within a specification that is written well, this distinction should track with whether (respectively) the test encountered an issue relating to functionality being evaluated (i.e. the system under test, within the assertion statement) or anywhere other than the functionality being evaluated.

For example, a non-zero result returned for a test run executed (by many common runners) in the command line don't usually provide clear signal as to what the mixture of failures to errors might have been for that run; text output produced by the test runner, though, frequently does. Some Web-based reporting distinguishes between errors and failures. The [Windy Road JUnit XML schema](https://github.com/windyroad/JUnit-Schema/blob/master/JUnit.xsd) specifically differentiates between [a result of `error`](https://github.com/windyroad/JUnit-Schema/blob/master/JUnit.xsd#L90-L92) and a [result of `fail`](https://github.com/windyroad/JUnit-Schema/blob/master/JUnit.xsd#L111-L113).

The more one needs to dig into the definition of a test, the finer details of implementation (either test code or production code) or anywhere else beyond test results and logging to determine either where (between test code and the system under test) an issue occurred or even what the nature of the issue was, the less efficient the test generally was as a source of data and/ or feedback. Assertion libraries help ensure that the contribution assertion statements make to these efforts clear and easy to follow.

### A Clear Summary of the Mismatched Comparison
When a comparison mismatch occurs during test runtime, an assertion library can generally be expected to display some sort of message outlining what the set of expectations was for the mismatch and how the values (often described as the _actual results_ or actual output) used in the comparison failed to match expectations.

Along with a clear distinction between `pass` and `fail`, a message clearly describing the terms of a comparison mismatch can help make it easy (also readable as _efficient_) to determine where a mismatch occurred within a failing test. 

With this in mind, and if it also seems agreeable that an assertion statement works by providing functionality with a _clear opportunity to fail_, it should generally be possible to compose an assertion statement in such a way that maximizes the amount of information provided. In the case of a failed assertion, promoting the likelihood of pinpointing from within the assertion where a failure occurred (while at the same time limiting the amount of in-depth troubleshooting that might need to take place) can often help make diagnosing a root cause easier (also readable as _more efficient_). 

Here is an example of a test failure message printed by Python's built-in `assert` keyword as reported by [pytest](https://www.pytest.org/):

```plaintext
    def test_that_true_is_equal_to_false():
        expected = True
        actual = False

&gt;       assert actual == expected
E       assert False == True

tests/test_with_assert_keyword.py:5: AssertionError
```

Here is another example produced in Java by [Hamcrest](https://hamcrest.org/JavaHamcrest/), in a test written using [JUnit](https://junit.org/):

```plaintext
TestMain > testTrueIsFalse() FAILED
    java.lang.AssertionError: 
    Expected: &lt;false&gt;
         but: was &lt;true&gt;
        at org.hamcrest.MatcherAssert.assertThat(MatcherAssert.java:20)
        at org.hamcrest.MatcherAssert.assertThat(MatcherAssert.java:6)
        at org.example.TestMain.testTrueIsFalse(TestMain.java:12)
```

In both examples, we get all of the following information:

- What the expected value was defined within the test.
- What the actual value was that the assertion statement used to compare against expectations.
- What the file and line number were encountered where the assertion statement that encountered a comparison mismatch.

Within the Python example, some extra care is taken to make it clear (between the `>` line and the `E` line) how expected- and actual values correlate with the values stored for the variables that were compared.

Both Python and Hamcrest give us some additional information here that generally isn't available with JUnit's `assertTrue()`: what the criteria were for the comparison that failed.

For example, if we tried asserting that `0` is greater than `1` using Hamcrest's `assertThat(0, greaterThan(1));`, the current release of Hamcrest would print output that looked like this:

```plaintext
TestMain > testZeroIsGreaterThanOne() FAILED
    java.lang.AssertionError: 
    Expected: a value greater than <1>
         but: <0> was less than <1>
        at org.hamcrest.MatcherAssert.assertThat(MatcherAssert.java:20)
        at org.hamcrest.MatcherAssert.assertThat(MatcherAssert.java:6)
        at org.example.TestMain.testZeroIsGreaterThanOne(TestMain.java:23)
```

This is slightly different than what JUnit's built-in `assertTrue()` would print for what is effectively the same comparison (`assertTrue(0 > 1);`) in the current release:

```plaintext
TestMain > testZeroIsGreaterThanOne() FAILED
    org.opentest4j.AssertionFailedError: expected: <true> but was: <false>
        at app//org.junit.jupiter.api.AssertionFailureBuilder.build(AssertionFailureBuilder.java:151)
        at app//org.junit.jupiter.api.AssertionFailureBuilder.buildAndThrow(AssertionFailureBuilder.java:132)
        at app//org.junit.jupiter.api.AssertTrue.failNotTrue(AssertTrue.java:63)
        at app//org.junit.jupiter.api.AssertTrue.assertTrue(AssertTrue.java:36)
        at app//org.junit.jupiter.api.AssertTrue.assertTrue(AssertTrue.java:31)
        at app//org.junit.jupiter.api.Assertions.assertTrue(Assertions.java:179)
        at app//org.example.TestMain.testZeroIsGreaterThanOne(TestMain.java:25)
```

While the level of detail provided here might seem insignificant (even possibly like noise), it's actually helpful as an additional source of signal that can help make identifying the source or nature of a mismatch easier (read _more efficient_). The Python example goes so far as to name the variables involved in the comparison mismatch. Both the Python- and Hamcrest examples also print what the criteria were for the comparison that encountered the mismatch, in addition to any of the other information.

Meanwhile, the most information the JUnit assertion statement provides is that there was a mismatch and (by way of the stacktrace) which code was ultimately involved in the mismatch.

## Assertion Libraries Provide APIs That Support Defining Custom Matchers
Although the idea has not been developed much thus far in this post, there is often some amount of work an assertion library performs under the hood to make the functionality it provides robust, consistent, and easy to use. And while well-rounded assertion libraries are generally prepared to do most of this work for most data types, use cases occasionally surface for which, despite the fact that it would be helpful to make use of the above, support doesn't exist for the particular use case.

We often define assertion statements in terms of single-line statements, and from those same statements (as well as the comparisons they perform) we expect one of two result statuses: `pass` or `fail`. It's how runtime connects the two that makes assertion libraries as valuable as they are subtle. Good assertion libraries don't just make this connection subtle, though; they generally also make the subtlety easy to navigate because the functionality provided within that subtlety is applied _consistently_ between the various matchers that support the lexical systematization that is likely (at least somewhat) unique to the library. This is somewhat remarkable on its own due to the wide variety of data types and use cases an assertion library is often tasked with handling and evaluating in order to produce clear signal.

For example, the logic to execute `.toEqual()` within Jasmine's integrated assertion library is (currently) spread (mostly) across three methods ([one](https://github.com/jasmine/jasmine/blob/bd9a3b23058ae2bd41992f0b703babc32949a954/src/core/matchers/toEqual.js), [two](https://github.com/jasmine/jasmine/blob/bd9a3b23058ae2bd41992f0b703babc32949a954/src/core/matchers/matchersUtil.js#L161-L169), [three](https://github.com/jasmine/jasmine/blob/bd9a3b23058ae2bd41992f0b703babc32949a954/src/core/matchers/matchersUtil.js#L170-L515)). Part reason for the complexity (as I understand, reading through the code) is the vast set of inputs (not just strings _and_ numbers _and_ booleans (_and_ at one point, [instances of `Error`](https://github.com/jasmine/jasmine/blob/bd9a3b23058ae2bd41992f0b703babc32949a954/src/core/matchers/matchersUtil.js#L194-L200)), but beyond that, nested instances of `Object`); another is the amount of painstaking evaluation and careful flow control that need to go into making a the type of comparison represented by the lexical statement `.toEqual()` understandable to humans who write- and read the statement.

Beyond this, assertion statements can be used to check for things like whether a particular method fired or (as noted above) whether an exception fires once a specific method is called.

Even with the availability of this extensive and complex matching functionality, though, not all data types lend themselves to comparison that is convenient for those responsible for test automation. Within a particular test automation framework, it might make sense to navigate complex data within runtime to enumerate the number of levels presented within a data tree (or, for example, the number of nodes that do not possess descendants) or count the number of events stored in a queue and expose that as a numerical value that can be compared against numerically (equal to, greater than, and so-on). Maybe the data structure is complex enough that it's not possible (or advantageous) to decompose the data structure (or extract a count from it) before attempting to make use of a built-in assertion. 

Whatever the use case, many assertion libraries make themselves available to _extension_ -- that is, it is often possible to extend any of the built-in matchers (or to reuse logic used to define matchers) in order to produce new assertion logic that continues to connect simple lexical construction to a limited set of test outcomes much the same way built-in functionality does within the assertion library.

## Conclusion
Assertion statements play a key role in producing signal (by way of test results) from which the data and feedback that automated tests are responsible for is gathered. When a test runner reports a result status of `pass` for a specification, any assertion statement executed within the test plays a role in producing this signal. Similarly, with a result status of `fail` (often as the result of an assertion mismatch -- contrast this with a test result status of `error`), assertion statements play a role in producing this signal, as well.

Between the roles assertion statements play within the code composition of a test, the roles they plays within test runtime, and the role tests play as a source of data and feedback related to the current functional state of work product, serve in essence as [the moment of truth where it's asserted either that the system under test has behaved as it's expected to or that it hasn't](/blog/?p=10). They serve as a key focal point (within the way an automated test is both composed and executed), [upon which (much like a target) the inquiry that a specification is responsible for executing is effectively trained](/blog/?p=16). And the declarativeness of any constraint the criteira present for either success or failure [serve as a sort of road sign pointing directly at either what should go right and (hopefully) what goes wrong if a test should fail](/blog/?p=20).

Assertion libraries contribute to test automation frameworks by delivering key support for making all of the above not only possible but in many cases also convenient and predictable. They deal specifically with supporting the definition and execution of assertion statements within a paradigm like this. Specifically, they provide:

- **A set of APIs usable to define assertion statements**, including the size of any aperture the level of specificity criteria for the assertion statement imposes on functionality. 
- **Some means of reporting assertion mismatches.** The primary operational role an assertion statement plays in test runtime involves comparing an expected value with an actual value, but in case of a mismatched comparison, and assertion library makes it possible to go beyond a simple `pass` or `fail` result to provide additional signal what went wrong.
- Some subset of functionality that makes the library extendable, including by **definition of custom search statements**.

Much like a reflector on a bicycle, an assertion statement should help make it clear what it's connected to. A well-written assertion statement helps make it clear (even at a distance) both how a test aims to compare actual output to expected output and what the result of an assertion was in runtime if output from the system under test by chance ends up somewhere (or, more likely, resembling something) unexpected.