---
title: "Test Parametrization: Exploring Reusable Test Design and the Benefits of Making Automated Test Code DRY"
publishDate: "2024-10-09T23:27:15-05:00"
coverPhoto: "daniel-klein-uehGpZefOBE-unsplash"
draft: false

---

It seems fairly often that I encounter test code in a pull request or in an existing file where a software developer has expanded existing test coverage by copying an existing test specification and adjusting a subset of values within the pasted duplicate.

I understand some of the rationale that this practice seems to follow. For one, if a specification occupies 25 lines in a file, copying the existing specification can be a low-cost way to take advantage of a working set of test operations (defined within the original specification) by adapting the copy to the new use case. In practice it's pretty low buy-in: just copy and paste (and adapt the duplicate; likely also modify the specification name), and you have successfully extended coverage.

The main problems resulting from this approach tend to surface when anybody responsible for the test attempts to do things that require reading test specifications and comprehending or comparing the contents of various test specifications that have been copy-pasted. For example, imagine that `test B` was created as a copy of `test A` (at the time `test B` was created, both were 25 lines in length, at which point we start with 50): are `test A` and `test B` relevant in the same ways as a source of data and/ or feedback related to functional state? How are they different? If `test B` fails intermittently and `test A` never fails (_ever_, which on its own seems peculiar), how might the differences between the two have bearing on the differences in reported test results?

Here efficiency in implementation has done a commendable job of reducing the front-end cost to establish automated testing, but only at the expense of any work that will depend on readability later on. Eventually, somebody will have to pay. And the more it will be necessary to read the specifications in order to compare, differentiate, rework, reorganize, and potentially remove any test (which generally remains undetermined until the need for any such work emerges), the more may ultimately need to be paid down the road.

On the surface, this looks like the same sorts of problems [Don't Repeat Yourself (DRY) tasks itself with solving in principle](https://www.linkedin.com/pulse/understanding-dry-principle-software-development-its-c-verma-pxzec). With a single, authoritative source of truth defining the logic for similar- and related test cases, it should be possible with a minimum of code to define logic to execute both `test B` and `test A` with an amount of code that is likely less than the sum of both methods defined individually, as well as to make the pattern extensible and adjustable to accommodate a possible `test C`, `test D`, and so-on with minimal need for additional complexity.

Most popular test runners support **parameterizing test specifications** -- that is, writing test specifications that accept a _set of parameters_ as a _test case_ that, when provided as a member in a list, a test runner will iterate through (the test cases) when executing the specification.

Here is an example of a working parameterized test in JavaScript (executed using Jasmine), for a simple method (no concerns about unexpected input here) tasked with multiplying two values:

<pre><code class="language-javascript">
const multiply_values = (v1, v2) => {
    return v1 * v2
}

describe(`when the multiply_values function is invoked`, () => {
    [
        { v1: 2, v2: 1, p: 2 },
        { v1: 2, v2: 2, p: 4 },
        { v1: 2, v2: 3, p: 6 }
    ].forEach(({ v1, v2, p: expected }) => {
        it(`returns a product of ${expected} when multiplying ${v1} by ${v2}`, () => {
            const result = multiply_values(v1, v2)
            expect(result).toEqual(expected)
        })
    })
})

</code></pre>

Not counting the `describe()` statement itself, this example code does the same work in ten lines that three copy-pasted `it()` methods would (as currently formatted) require twelve lines for. The example code is (generally, minus variable assignments) less redundant, and it lists the input values and expected results all in a unified and easy-to-parse truth table. As a bonus, it fills in a descriptive name for the test based on values provided within the test case.

This post will explore the ways that test design supporting specification parameterization (specifically as a means of embracing DRY) can help make test code more efficient, both as readable code and as tests.

## What is DRY, and is it Valuable in Code?
In software development, the **Don't Repeat Yourself (DRY)** principle generally supposes that the greater the number of times code defines the same functionality (verbatim) independently, the more redundant any such independent definition likely is. In the abstract (and was defined by the originators of the principle), DRY promotes use of a **single, unambiguous, authoritative representation** for functionality, code patterns, and data. In practice, though, the acronym DRY is frequently used as a homonym of the adjective _dry_, at which point useage refers to the degree to which code is DRY (for example, "more DRY" or "most DRY", or other renderings of the comparative and superlative forms) as a description of the degree to which code promotes this principle.

In principle, the more redundant definitions of functionality can be extracted and encapsulated into shareable patterns, the simpler the resulting code should be as a result of condensing verbosity. This also has the benefit promoting the reusability of DRY code. To a degree this explains (to some degree) not only why many [primers for those new to programming explain functions in these terms](https://www.freecodecamp.org/news/java-methods/#heading-what-are-java-methods); it also provides something that resembles a backstory for many of the [benefits provided by Object-Oriented Programming at a fundamental level](https://www.linkedin.com/pulse/4-pillars-object-oriented-programming-diego-cardoso-de-melo-xmk5e).

Arguments in favor of DRY code design tend to look a lot like this:

_Code that embraces DRY is easier to read and maintain._

- References (like method calls) link back to the authoritative (shared) definition as a single source of truth.
- Because there is a single source of truth for shared definitions, code tends to be less verbose.
- Links between the initial definition and calls to that definition (like a method call or instantiation of a class) make it possible to see all of the places where shared definitions get used.
- DRY code can be easier to debug, because a shared definition serves as a single point of failure.

_Code that embraces DRY benefits from being more consistent._

- Shared definitions should be **easier to test** where they reduce the complexity of code that needs to be tested. Let's say we wanted to test view builder functionality that was employed at five different places in code. If the builder functionality was made reusable (and defined in just one place), it should be possible to test (for example at the unit level) the code responsible for all five uses of the method. If the same functionality were implemented ad-hoc in all five places, testing the solution thoroughly would likely involve exercising operational logic that made use of each of the five places where functionality was defined.
- Generally a **regression** should be **more noticeable** with shared definitions. If, within a solution, a shared method is called from five different places in code and that method fails to function as expected, there's a chance that evidence of the break will show in at least any (maybe all) of the five occurrence of where the shared method gets called. Meanwhile, for ad-hoc individual definitions of the same functionality, a break in one place may not be visible elsewhere.

At the same time, the same way there is disagreement on nearly everything in software development (including testing), there is also disagreement as to whether DRY is always a net benefit in code design. Whether the argument is that DRY is always problematic (because, for example, constraints for a single authoritative definition of functionality can be expected to lead to complex architecture, unnecessary abstraction, and difficult-to-follow dependency relationships) or that [DRY is sometimes problematic (depending on how it is used, it presents an opportunity for premature optimization and code that cannot be read in a linear fashion)](https://medium.com/bootdotdev/the-pros-and-cons-of-dry-code-1a3ee7838943), or even that the assessment that shared code is simpler to test (see above) is both contextual and subjective, it is not much of a challenge to find dissenting opinions that are generally credible.

Some have also suggested a [WET (Write Everything Twice) principle as an alternative to DRY](https://www.deconstructconf.com/2019/dan-abramov-the-wet-codebase): in order to avoid premature optimization through DRY, it may be worthwhile to accept at least some redundancy, whether just for the short term or potentially indefinitely.

Although the aim in this post will be to explore the positive trade-offs of promoting DRY through test parameterization, it will not be to litigate (or even enumerate) the potential negative trade-offs. In my experience, any negative trade-offs generally track fairly closely with the negative trade-offs of DRY itself, save for a couple that I describe in the section outlining benefits.

## What Is a Parameterized Test Specification?
A parameterized test specification is a type of **test specification** (very often a method designated using [APIs exposed by the test runner](/blog/posts/understanding-test-automation-frameworks-what-is-a-test-runner/) as one containing operational logic that should be used when executing the automated test the method _specifies_) that accepts a set of parameters serving to define a test case that the specification should accept as input for a single iteration of execution.

The general idea making this work is that, if a programmer can extract values used within the specification to a point outside of the specification, it should be possible to take advantage of the same operational logic for a series of test cases, each with its own set of **parameters**. Within the example provided in the introduction, the array the `forEach` statement loops through defines three test cases, each with its own set of parameters. As Jasmine executes a test run, it will iterate through the array of test cases one by one and execute the `it()` method once using data within the current iteration as a set of parameters to execute `it()`.

Here is a working example (written in Python) using Pytest as a runner to define tests very similar to what was provided in the introduction:

<pre><code class="language-python">
import pytest

def multiply_values(v1, v2):
    return v1 * v2

test_cases = [
    {"v1": 2, "v2": 1, "p": 2},
    {"v1": 2, "v2": 2, "p": 4},
    {"v1": 2, "v2": 3, "p": 6},
]

@pytest.mark.parametrize("test_case", test_cases)
def test_multiply_values_returns_expected_product(test_case):
    v1, v2, expected = test_case["v1"], test_case["v2"], test_case["p"]

    result = multiply_values(v1, v2)
    assert result == expected

</code></pre>

Here is an example using Cucumber as a runner to define what looks like a very similar set of tests:

<pre><code class="language-gherkin">
Scenario Outline:
  Given v1 is provided a value of &lt;v1_value&gt;
  And v2 is provided a value of &lt;v2_value&gt;
  When the multiply_values method is used to multiply v1 and v2 together
  Then the product of the multiplication should be &lt;expected_product&gt;

Examples:
  | v1_value | v2_value | expected_product |
  | 2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| 1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| 2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
  | 2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| 2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| 4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
  | 2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| 3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| 6&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|

</code></pre>

In these examples, parameterized test specifications (much like general program code designed in a manner that promotes DRY) enjoy many of the same benefits as [parallel construction in natural language](https://en.wikipedia.org/wiki/Parallelism_(grammar)). Taking advantage of an opportunity to condense a series of otherwise-verbose statements into a well-organized compound statement can help make sentences (like the one you are reading right now) describing complex relationships simpler, easier to follow, and generally more efficient as a result. Not only does the printer require less toner (or the speaker less breath) with parallel construction; the reader or listener should hopefully be able to recognize with relative ease how serialized items, phrases, or clauses relate to each other within a (parallelized) grammatical construction in order to be able to unpack meaning efficiently.

As is also often the case with parallel construction, the cost of efficiency in parameterized tests may be complexity, but with the right structure and approach to organizing code that complexity can hopefully be made reasonably simple.

## What Are the Benefits of Automated Test Design That Embraces DRY Through Test Parameterization?
DRY is a principle that can be used in the design of program code of (as far as I am aware) nearly any type. As noted above, DRY presents both positive and negative design trade-offs to code that takes advantage of it.

Even though they are very often _defined using code_, automated test specifications are not _valuable only as code_. They deliver value as tests, which execute in service of distinct inquiries and provide data and feedback that can be used to inform visibility into current functional state of work product. Whether these tests serve as checks (for example, executed in CI) or as a medium for exploratory testing (for example, performed in a local IDE or via the command line), the sort of parallel construction and DRY code design that parameterized testing make possible can provide benefits both to the design of test code and to the design of tests that depend on that code.

### Code Design Benefits: Opportunities for Readability, Simplicity, and Stability as a Result of DRY Code
Test code that makes sensible use of parameterized test design can expect to take advantage of many of the same benefits that general program code enjoys as a result of embracing DRY. Because the code is condensed, it tends to be simpler, easier to follow, as well as easy to organize, extend, and reuse if needed. The same way we expect the runner to unpack (or [`@Unroll`, as Spock defines it](https://spockframework.org/spock/javadoc/2.3/spock/lang/Unroll.html)) individual cases in runtime, with any hope a well-written parameterized test specification should lend itself to a similar sort of unpacking by a human reader.

As explained (somewhat extensively) above, this is not necessarily a slam dunk (neither, from experience, is DRY), and many of the same negative trade-offs that DRY presents on its own are worth considering when designing parameterized test specifications. For example, it can be easy (even with the best intentions) to end up with a suite of parameterized tests that nobody understands because, although the specifications do an excellent job of making the code that defines their operations functionally reusable, their current implementation promotes reusability at the expense of test readability, atomicity, or declarativeness.

In addition, I've found that when I personally write parameterized specifications, I will occasionally check the value defined for a parameter within a test case (within the examples provided in this post, something like `v1` or `v2`) within the method body for some sort low level conditional flow control or [even an integrity check that may result in throwing an error](/blog/posts/making-the-most-of-throwing-errors/), depending on the particular case. Put simply: sometimes I end up with if-thens that key off of individual values passed as parameters (which may lead to additional operations case-by-case) for the current test case. This presents its own set of design considerations, including whether the resulting parameterized test code is potentially less simple (and in some cases more challenging) to follow.

My general experience has been that as long as a test remains **declarative** (that is, the way any definition of operations including what gets evaluated is kept explicit or clearly intentional in code) and the fewer times adjustments like this need to be made within a single specification, the less likely this will be problematic for either readability or the integrity of the code pattern that the specification relies on.

As a rule of thumb, though, I attempt to weigh whether any complexity presented within a parameterized test specification is any more- or less complex than having to diff multiple copy-paste iterations of the same specification -- either with a diff tool or without.

### Test Design Benefits: Consistency, Extensibility, and Adaptability
When test specifications are written in such a way that any iterative test case follows a given code pattern, test design _couples_ the execution of each applicable test case to that code pattern. Generally this works in a manner that keeps test runtime consistent for any test case making use of the same pattern. Where the definitions of five different copy-paste specifications might drift over time, five test cases executed through a parameterized test specification all execute using the same code, because the definitions of the tests is coupled to the pattern established within the shared code.

For reference, _uncoupling_ a particular test case from a well-written specification should be as easy as removing it from the shared specification and creating a new one. No harm in copy-and-paste here if it actually promotes readability.

Also for reference, the last four paragraphs of the previous section walk through reasoning for some potential exceptions to how and whether this is valuable.

Where one of the primary benefits commonly touted by advocates of test automation is _consistency in test runtime_ (the other being _speed of execution_), though, the benefits of sensible coupling in this manner should hopefully be recognizable as a relatively easy win.

At the same time, the moment a test specification makes itself open to parameterization, it also makes itself easily extensible and adaptable. **Extension** for a test specification looks something like this: _If we can execute one relevant test case using the same code, why not three (as long as they're relevant)? Why not five?_ Meanwhile, **adaptation** supposes that either the same test code can be applied as-is to a similar test case or that it can be updated slightly to accommodate a similar case that doesn't follow the same pattern 100%.

When I (personally) write test specifications, anything I can do to make sure variables are assigned clearly (usually at the beginning) in such a way that they can easily be identified and potentially extended or modified makes the specification _open to parameterization_, if not just by updating the variable assignment (no need to pass in test cases). The easier this makes swapping in a list of test cases for a single case, the better.

At the same time, though: the easier this makes simply swapping _one set of values or parameters_ in for another (no list of cases required), also the better. As a software solution responsible for supporting automated testing (even if more literally _executing_ test operations _as defined_), the specification now supports multiple _testing use cases_ (that is: use cases directly supporting testing activity) without compromising the integrity of the code pattern the specification relies on.

For a simple set of tests exercising something like [the in-memory test data management system I've written about previously](/blog/posts/design-overview-in-memory-generic-test-data-managment-in-javascript-using-lokijs/) as (developed as part of [a mock backend solution for UI testing](/blog/posts/how-i-improved-testing-stability-and-reduced-test-runtime-by-90/)) (where `RecordSet.create(snapshot)` is expected to clone values from the snapshot passed to it as a means of protecting snapshot data provided in the original argument from mutation), a limited suite of specifications open to parameterization can look something like this:

<pre><code class="language-javascript">
const peopleData = new PersonRepository('testData.people')

describe(`when the CREATE verb is used to save a new record snapshot`, ()=> {
  const person = { firstName: 'Paul', lastName: 'Person' }
  let matchingRecord

  beforeAll(()=>{
    peopleData.create(person)
    matches = peopleData.collection
      .chain()
      .find({ firstName: person.firstName, lastName: person.lastName })
      .data()

    if (matches.length !== 1) {
      throw Exception(`Expected one match for person defined as ${JSON.stringify(person)}, but found ${matches.length}: ${JSON.stringify(matches)}`)
    } else {
      matchingRecord = matches[0]
    }
  })

  it(`persists the expected value for firstName`, ()=>{
    expect(matchingRecord.firstName).toEqual(person.firstName)
  })
  it(`persists the expected value for lastName`, ()=>{
    expect(matchingRecord.lastName).toEqual(person.lastName)
  })
})

</code></pre>

Here, instead of settling for a one-off test against a specific real-world use case, this code provides a reusable subset of tests that can potentially be made use of locally (i.e. in an IDE on a local machine as opposed to in CI) to test any set of values specified for `person.firstName` and `person.lastName` (even if, for example, Paul was given a last name of `PurpleMonkeyDishwasher` or even a first name of `Paula`) in addition to the values currently persisted in VCS (which is what gets executed in CI).

At the same time, though (along the same lines as [organizing automated tests around method calls in such a way as to collate trips to external systems](/blog/posts/collating-test-methods-to-limit-trips-to-external-systems-in-automated-tests/)), this pattern allows for extension either by way of defining test cases as input to a `forEach` statement (for which the `describe()` statement would run within the callback) or by way of additional `it()` methods in the callback for the `describe()` block. To whatever degree it might be valuable to add elements, change values, or add checks in support of the inquiry (or _inquiries_) the `describe()` block may be tasked with executing on behalf of, this `describe()` block is ready for it.

Here, sensible embrace of DRY produces test design that is both extensible and adaptable. And it leaves the `describe()` block open to parameterization if desirable. As currently written this is no longer just a set of tests; it now works in essence like a small machine ready to serve as any number of testing use cases while still playing within most conventional boundaries defining what makes a good automated test.

By comparison, consider the extensibility and adaptability of coverage provided by copy-pasting similar-looking test specifications.

## Conclusion
Imagine listening to a description of how somebody harvested corn from a field, where it was necessary to restate every time how the corn harvester or combine passed along a particular subset of rows. _Let me know if you've heard this one before._

For somebody listening to (or even reading) a description like this, it seems like it would be a challenge not to gloss over details (even refrain from interjecting) sometime during or after the second pass. For somebody responsible for providing this explanation, it seems like it might also be a challenge to keep track of describing each pass individually. It would likely be a lot easier just to summarize: to condense similar statements and provide a clear description of how the corn was harvested _row by row_, until the field had been cleared.

To be fair, maybe it was a crew job, at which point multiple machines were used to clear the field. That reads a lot like parallel execution, which unfortunately is out of scope for this post.

In a similar way, parameterized test specifications allow for test operations to be defined _row by row_. Sequentially, for each set of parameters (each representing a distinct test case), a test runner will conventionally execute a copy of the shared test specification once (as though it had been copy-pasted), using the current set of parameters as input. When test code ultimately needs to be read (for example, during troubleshooting or when reworking existing tests), embracing this sort of construction can help make it clear to readers (and potentially other developers) what _row by row_ looks like without needing to explain (or read) progress over the entire field verbatim.

That being said, though: it pays to dig a little deeper than the surface layer of this simple feature (that, again, many popular test runners support) to get a clear sense of how the feature's use may be valuable to the business of test automation. Part of what makes test parameterization work as described in this post is the way in which it allows both writers and readers of test code to embrace DRY in a way that (hopefully, depending on how shared functionality is implemented) presents a net benefit (as something resembling parallel construction in natural language) to readers, to testers, and to other software developers.

If automated testing serves as an investment (into developing visibility into the current functional state of work product that is expected to be both serviceable and efficient), it (generally) pays to be clear on the front end (even if inductively) what the likely costs and benefits of design decisions involved in that investment are expected to be. If, beyond running them, some of the most time-consuming work that automated tests can be expected to require throughout their service lives involve understanding how the code somebody else (or even we ourselves) wrote at some point in the past provides value as a test now, making test specifications easy to read can be an easy way to reduce anticipated costs proactively.

At the same time, if a test specification is written in a manner that makes it open to parameterization (or, otherwise: reuse), this lends itself not only to expanded readability but also to extension and adaptation as code that looks as simple as a single organism but potentially covers an entire field (or possibly a landscape) of possible test use cases.

Those test use cases may even include **data-driven testing**, which this post has (admittedly) sidestepped somewhat intentionally.

So the next time it seems tempting to copy-paste an existing test specification as a means of expanding coverage, it may be worthwhile to stop and examine more clearly what you intend to plant. That, and perhaps also what you expect to grow in its place.