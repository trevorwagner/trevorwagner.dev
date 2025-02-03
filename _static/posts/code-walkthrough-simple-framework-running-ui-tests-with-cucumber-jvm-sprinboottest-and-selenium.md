---

title: "Code Walkthrough: Simple Framework Running UI Tests with Cucumber-JVM, SpringBootTest, and Selenium"
publishDate: "2023-07-08T15:31:00-05:00"
coverPhoto: "alex-guillaume-IWnuBhG_y34-unsplash"
draft: false

---

For this post I'm going to try something a little more concrete and a little closer to home for anybody interested in test automation. I'm going to talk about how I built [a demo framework I host on GitHub and why I made the choices I did to build it](https://github.com/trevorwagner/spiegel-junit-med).

If it helps, I named the framework **Spiegel**, which is the German word for *mirror*.

## Introduction/ Problem Description

The system under test I will be using for this demonstration will incorporate two pages from the DuckDuckGo search engine:

- [DuckDuckGo's landing/ main search page](https://duckduckgo.com/).
- [A Search engine results page](https://duckduckgo.com/?q=why+can%27t+everybody+just+say+%22duck+duck+gray+duck%3F%22&va=v&t=ha&ia=web).

For anybody potentially unfamiliar with a search engine, these pages use a design that has become ubiquitous among search engines since at least the 1990s: once you enter a search query on the main page and execute a search, the search engine results page will show results returned by the search engine for the search query.

## General Testing Strategy

There are two sets of goals in the approach to this exercise: short term goals and long term goals.

The short term goals for this exercise involve demonstrating the testing system (and with it my ability to write a usable testing system). The demonstration will involve exercising the UI on the pages on DuckDuckGo listed above. We will be exercising the pages from the perspective of general common use cases (effectively this is happy path). This strategy will not involve extensive coverage, and it will not involve extra functionality like user management, session management, or producing or submitting test results. In essence the goal here is a quick and dirty "hello world."

The long term goals for this exercise involve architecting something that, beyond immediately useful as a demonstration, also gives users something they can tinker with to see how it works. So beyond demonstrating "hello world," I'd like to **focus a little on reusability**. For example, if somebody would like to test against a search terms other than the ones I've provided within the feature files I've provided, they should be able to create another Cucumber scenario/ scenario outline, add their custom search text, and run a test against that, as well.

I've also done my best to make the code as cleanly modularized and easy to follow as possible. This also provides **limited extensibility** to the framework.

To implement this strategy I will be using a stack that uses the following libraries:

- [Gradle](https://gradle.org/) to define tasks/ set up test runtime.
- [Cucumber-JVM](https://cucumber.io/docs/installation/java/) as a test runner. For anybody unfamiliar, Cucumber is a BDD test runner that allows tests to be defined as human-readable text.
- [SpringBootTest](https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/test/context/package-summary.html) to provide inversion-of-control container to make persisting things like the WebDriver connection and any additional data that needs to survive Cucumber's step lifecycle easier.
- [Selenium](https://www.selenium.dev/) to interact with a Web UI by way of a connection between test code and a Web Browser. There are alternatives (Playwright is one I like) that we could use here instead of Selenium. Chef's choice, and beyond our architectural goals for this framework, we're just trying to deliver "hello world."
- [Hamcrest](https://hamcrest.org/) as an assertion library. I like the assertions I use to look as much like natural language as possible (it helps make them more readable).
- [JUnit](https://junit.org/), both to bootstrap Cucumber.class and to run unit/ integration tests against the framework. At the time I needed JUnit 4 in order to be able to bootstrap Cucumber; FWIW I used JUnit 5 for unit- and integration tests.

If you'd like to see the versions of everything I'm using I actually make them as easy as possible to review (this helps me, too) [within `build.gradle`](https://github.com/trevorwagner/spiegel-junit-med/blob/2f2ce3175bea3d518b42f1d02d7bde142d525b48/build.gradle#L7-L23).

## Organizing the Project as Ready to Modularize

I have personally had the experience of defining new tests in more than one expansive, monolithic JVM-based test framework, then configuring the framework to point at the appropriate test system, then pressing enter to execute. After that... (we wait)

Then... (we wait)

Then... (we wait)

And we continue to wait (maybe three minutes, maybe longer -- who knows) while the whole project compiles, including potentially running any tests against it. Only then do we get to execute tests. Hopefully we didn't encounter a compilation error or make a mistake that would require us to stop execution (hopefully the tests don't fail while we're at it), because then all that time we spent waiting would effectively have been wasted.

For now let's not talk about potentially running this framework in cloud infrastructure or a CI service that charged by the compute cycle.

A few years ago I found a pattern (it looks like it's since been taken down by the author) where the software engineer modularized parts of the framework, each (defined for Maven -- not Gradle) with its own individual `pom.xml`:

- [glue](https://github.com/trevorwagner/spiegel-junit-med/tree/main/src/main/java/io/twagner/spiegel/cucumber/glue): Store Cucumber step definitions, lifecycle hook code, and code directly tied to running Cucumber steps.
- [pageobjects](https://github.com/trevorwagner/spiegel-junit-med/tree/main/src/main/java/io/twagner/spiegel/pageobjects): Store only page objects (if you're unfamiliar with page objects see below) used with Selenium (or your applicable UI interaction framework).
- [framework](https://github.com/trevorwagner/spiegel-junit-med/tree/main/src/main/java/io/twagner/spiegel/framework): Store test support code that doesn't easily fit into the two other groups. I store my settings classes in here, as well as code to support retrieving an instance of WebDriver for use in testing.

The original example I found used a fourth module. I can't remember clearly anymore what it was. It might have been for the feature files themselves (so that an update to feature files didn't result in glue code compiling -- if I'm correct there the module would have been called **tests**).

The main project also used its own pom.xml (that defined how to run tests) that consumed the subordinate modules.

I've taken this with me because I thought it was very thoughtful: in larger frameworks it cut down overall compile time because rather than compiling the whole project it compiled the relative individual module if a file changed. It's definitely not the first time I've seen software engineers break test functionality down into modules or use an independent test support library.

When I'm early on in development (usually prototyping), I just use folders: when the project is this small, compiling modules like this individually increases overhead. When I'm ready, I'll define `build.gradle` files for each individual module. And if I need to break the modules out into their own libraries I am ready to, because I've proactively modularized my code.

If I was still worried about cycles in CI here I would likely convert the modules to independent libraries. So now in addition to doing right by local testers we could also do right in CI.

## Gradle and JUnit

Defining jobs that run tests is where I generally start writing regardless of which runtime it's for: once I have usable test runtime, I can build and validate what I need within it. I'll start with `build.gradle`, add dependencies (I use Maven Central Repository for my URLs), wire up the test runner, and make sure I can get a successful run with something like assertThat(true, equalTo(true)); that I can bit-flip, to make sure both that tests pass and fail as expected.

Within `build.gradle`, I've chosen to create a small registry where I list the version numbers of certain libraries I use. Instead of leaving version numbers within the listing for every individual dependency, this helps me see at a glance which version of Selenium (for example) I'm using in the framework. Or JUnit. Or Spring. In addition, some libraries share versions with their dependencies; use a specific version of one library is coupled to use of the same version of another library. So to keep all of my Spring Framework dependencies on the same version number, I store the shared version number once and refer to the variable throughout `build.gradle`.

Before moving on there are two more things I'd like to point out here:

- I add JUnit twice:
 - [Junit 4 (via cucmber-junit)  as `Implementation`](https://github.com/trevorwagner/spiegel-junit-med/blob/2f2ce3175bea3d518b42f1d02d7bde142d525b48/build.gradle#L45-L46) (to add it to CLASSPATH for `runCucumberTests`). I use JUnit to bootstrap Cucumber (more in a minute).
 - [JUnit 5 as `TestImplementation`](https://github.com/trevorwagner/spiegel-junit-med/blob/2f2ce3175bea3d518b42f1d02d7bde142d525b48/build.gradle#L81-L82), so that it will be added to CLASSPATH (and can be invoked) when using `./gradlew test`.
- [I run JUnit as `JavaExec` task within Gradle](https://github.com/trevorwagner/spiegel-junit-med/blob/2f2ce3175bea3d518b42f1d02d7bde142d525b48/build.gradle#L93); JUnit [bootstraps Cucumber here](https://github.com/trevorwagner/spiegel-junit-med/blob/8412dbd62fb6a99a549ec2bb0eca0a4021013667/src/main/java/io/twagner/spiegel/framework/suites/SuiteParent.java#L6) (which [inherits from a parent class in order to define options for Cucumber](https://github.com/trevorwagner/spiegel-junit-med/blob/8412dbd62fb6a99a549ec2bb0eca0a4021013667/src/main/java/io/twagner/spiegel/framework/suites/AllTestsSuite.java#L5-L9)).

My reasoning for both of these decisions is that I believe strongly it's important to test code used to define the test framework as well as the system under test. If test code cannot evaluate the system under test as expected because of an issue in the test code, then all of the time (and resources) used to compile and run the framework to the point that an error has occurred have effectively been wasted. I probably wouldn't test imperative calls to Selenium much independently. But for things like user management, for translating text to values (if it's not simple), and even custom marchers, I find that the value in using a test framework I am confident in outweighs the expense of setting up tests against it. I'd recommend that anybody test their test code, their test doubles, test mocks, and so on.

By bootstrapping Cucumber from JUnit (again: run as a JavaExec task), it frees up the built-in Gradle task `test` (i.e. `./gradlew test`) for testing code used to define the framework itself. Once we run the `test` task, JUnit 5 takes over and runs its own tests (from the place we'd normally expect to see unit- and integration tests).

So before we move on, let's add **testability** to the architectural "ilities" we'll be using to define the architecture used to implement our testing strategy.

## SpringBootTest

Cucumber does a great job of making the building blocks to define a test interchangeable: if you provide a step/ line of text within a feature file that Cucumber matches, Cucumber will run the code associated with that step any time it encounters the step in test runtime. In exchange for that, Cucumber (in my experience, particularly Cucumber-JVM) tends to make persistence of state within test runtime a challenge to maintain and track on its own. To be clear, I believe this is more Java and less Cucumber. I've also found it sometimes be a challenge to attempt to rely on built-in functionality to store things like test run configuration and WebDriver instance; any time I try, I instantiate a new Web browser instance (including local web driver process when run locally) every test. That's not sustainable by any means.

For a solution to this (that also provides a pattern that is ready for easy reuse), I use Spring Framework to provide a unified inversion-of-control container to store state across my framework. Spring makes a library available called SpringBootTest that works specifically within tests; within the Spring container this provides, I can persist an instance of WebDriver, my configuration, and potentially anything else I need.

For anybody not familiar with Spring or Inversion of Control, it might be worthwhile to get familiar before trying to use SpringBootTest. For a beginner's tutorial on Spring I recommend [this YouTube series, courtesy of Cave of Programming](https://www.youtube.com/watch?v=PMX6HrdrnrY&list=PLIkhEkCcTUijrqkq8hZnjazsDyDm6sJ-A).

In order to make this work, I needed to implement two more classes: [`SpringBootIntegrationTest`](https://github.com/trevorwagner/spiegel-junit-med/blob/ead45a355dd58d3449116a4339856a21980ba985/src/main/java/io/twagner/spiegel/cucumber/glue/SpringBootIntegrationTest.java) and [`SpiegelFrameworkContext`](https://github.com/trevorwagner/spiegel-junit-med/blob/main/src/main/java/io/twagner/spiegel/framework/context/SpiegelFrameworkContext.java). SpringBootIntegrationTest provides instructions to carry systemwide system state (for the current run of the test framework) on fields [`frameworkConfig`](https://github.com/trevorwagner/spiegel-junit-med/blob/ead45a355dd58d3449116a4339856a21980ba985/src/main/java/io/twagner/spiegel/cucumber/glue/SpringBootIntegrationTest.java#L23) and [`driver`](https://github.com/trevorwagner/spiegel-junit-med/blob/main/src/main/java/io/twagner/spiegel/framework/context/SpiegelFrameworkContext.java#L23) that get instantiated during runtime (from Spring's IoC container) via the `@Autowired` annotation to call the runtime instance defined within `SpiegelFrameworkContext`. Every Cucumber step definition class I write (namely [`DuckDuckGoHomePageSteps`](https://github.com/trevorwagner/spiegel-junit-med/blob/2f2ce3175bea3d518b42f1d02d7bde142d525b48/src/main/java/io/twagner/spiegel/cucumber/glue/duckduckgo/DuckDuckGoHomePageSteps.java) and [`DuckDuckGoSerpPageSteps`](https://github.com/trevorwagner/spiegel-junit-med/blob/main/src/main/java/io/twagner/spiegel/cucumber/glue/duckduckgo/DuckDuckGoSerpPageSteps.java)) inherit from `SpringBootIntegrationTest`.

So within this implementation, one shared instance of WebDriver gets autowired to every class that implements UI steps. One instance of the framework configuration gets autowired (rather than, for example, read from file every time) to the step definition class.

## WebDriverFactory

[`WebDriverFactory`](https://github.com/trevorwagner/spiegel-junit-med/blob/768ccd3d3a9a052ed741f9cd996cb9c9d7213bdd/src/main/java/io/twagner/spiegel/framework/webdriver/WebDriverFactory.java) is not my idea; it's a pattern that as I understand it has been available for public use for some time. In essence, it solves problems related to the fact that any instance of a WebDriver browser connection is somewhat specific to the particular Web browser (Safari, Firefox, etc.) being used. Even within a specfic browser's version history, some versions support configuration options that others do not. Each browser provides a slightly-different API for configuration of that browser, but once the browser is running (and a connection has been established that makes the browser available during test runtime), the connection to that browser in test runtime makes use of a unified API.

So, in essence: I can use the same calls (regardless of browser) to interact with a browser once I have it, but different calls to configure the browser while attempting to establish a connection. The problem here is that all I want is a browser, and I don't want the complexity of having to wire up a browser in a manner specific to that browser in order to be able to use it. Instead I'd like to be able to provide instructions interchangeable enough that I can pass arguments to say "now run the same tests with Safari" or "now run the tests with Chromium version 98.something". I should be able to set that in a configuration file (or pass it with a command-line argument) at a high level and expect that the framework does whatever low-level work (in response to the settings I've passed) to wire up the browser I need.

WebDriverFactory uses the [Factory pattern](https://en.wikipedia.org/wiki/Factory_(object-oriented_programming)) to provide a level of abstraction that can be used to provide an interface for configuring browsers at a high level via a unified API and "just get a browser" (all I needed to begin with). In addition to this, I created a Java Enum (called [`SupportedDriverTypes`](https://github.com/trevorwagner/spiegel-junit-med/blob/6976a1d941e1361de2663de439d00c87504700e4/src/main/java/io/twagner/spiegel/framework/webdriver/SupportedDriverTypes.java)) to store browser names: if you want to describe Firefox anywhere in the framework, for example, just use `SupportedDriverTypes.FIREFOX`.

I like WebDriverFactory enough that I actually ported it to JavaScript at one point. Sometimes when all I want is a browser, and the only tool I have to get it is JavaScript, I can provide a unified interface there, too.

## Selenium Page Objects

Page Objects are classes that provide abstraction for Web pages for use in test runtime. I'd characterize them as an example of the [Facade pattern](https://en.wikipedia.org/wiki/Facade_pattern). The idea is that, if you encapsulate instructions to interact with a page or find elements on a page within a single class, that class becomes a toolkit with a unified set of tools that can be used any time you would like to interact with the same page.

So, for example:

- If you'd like to find an element on the page, you can reuse the instructions to locate that element within in a page object.
- If you'd like to perform an action like submit a search, you can reuse the instruction to perform that action within a page object.

What's more, let's say the developers responsible for the system under test change something on one of the pages that invalidate either the locators or something else within the page object. Because test code is abstracted and stored centrally, it wouldn't take long to update test code to adapt to changes in the system under test.

In my experience, page objects are used with Selenium more than with other UI interaction tools. I tend to use them as much as I can with Selenium (the more code gets successfully reused the more viable it likely is), but I've used them successfully elsewhere, as well.

- Page objects are particularly helpful when using Cucumber for two reasons:
- Encapsulating complex operations within a utility class helps keep Cucumber step definitions simple.

Page objects can be used to provide their own high-level API, so that low-level processes are described in terms of a domain understanding of either the technical process or the value to the system.

There's more going on here (like how I use `@CachedLookup` to discourage looking up element references every time Selenium needs to find an element). For now though, this is enough.

## Cucumber Step Definitions/ Support Code

Once I have everything else set up, I can start writing Cucumber step definitions that interact with the page objects (thereby the browser) to do things like submit a search query and read the search result page. It took a lot of work to get here, but this is where I wanted to be.

Likely I already have a couple step definitions I've written to validate the test framework -- basically something like "it works!" Once I have working step definitions for the system under test I'll probably throw these away.

For the framework demo itself, I created two step definition classes: [one for the DuckDuckGo main search page](https://github.com/trevorwagner/spiegel-junit-med/blob/2f2ce3175bea3d518b42f1d02d7bde142d525b48/src/main/java/io/twagner/spiegel/cucumber/glue/duckduckgo/DuckDuckGoHomePageSteps.java), and [one for the DuckDuckGo search result page](https://github.com/trevorwagner/spiegel-junit-med/blob/main/src/main/java/io/twagner/spiegel/cucumber/glue/duckduckgo/DuckDuckGoSerpPageSteps.java). Each step definition class also carries an associated page object for the respective UI Page targeted by the respective step definition class (here are the page object for main page and [the page object for search results page](https://github.com/trevorwagner/spiegel-junit-med/blob/2f2ce3175bea3d518b42f1d02d7bde142d525b48/src/main/java/io/twagner/spiegel/cucumber/glue/duckduckgo/DuckDuckGoSerpPageSteps.java)).

### Testing Conversions of Ordinal Expressions

In order to provide reusability to the tester, I needed to find a way to convert ordinal expressions for `1st`, `2nd`, `3rd`, etc. into numerical values. Beyond this, I recognized the advantage of converting specifically to zero-index: because calls to Array, List, and other data structures in Java (and for the record: not just Java) tend to use zero-index values to return the nth member, it seemed like my alternative was to work with this (to translate words to zero-index proactively) or against this (use only natural numbers like 1 and higher and convert immediately before calling zero-index). The former seems a lot less error-prone, even if it's not completely intuitive.

I decided to go with the former and be proactive about zero-index: `1st` will convert to `0`, `2nd` will convert to `1`, and so-on. I also chose to leave the door open to get the natural number (as opposed to zero index) without the consumer needing to do the math. I wrote [`OrdinalNumber`](https://github.com/trevorwagner/spiegel-junit-med/blob/main/src/main/java/io/twagner/spiegel/cucumber/glue/support/languages/en/OrdinalNumber.java) to cover both cases.

Although I don't personally believe I do a lot of processing here, I see an opportunity to get confused about what is expected to happen when humans evaluate this code. Probably not by me, but still. To guard against potential regressions in this functionality if somebody tries updating the code defining the functionality (or in case of an upstream change however unlikely that may seem), I decided it was a good use of time to [write tests against the functionality this code defines](https://github.com/trevorwagner/spiegel-junit-med/blob/2eb6fcb9b94a70ca6de3dc516d61fc1a77a5422a/src/test/java/unit/io/twagner/spiegel/cucumber/glue/support/languages/en/OrdinalNumberTest.java).

### Polarizing Expectations

Should it, or should it not? For me, being able to ask questions like this in terms of yes-or-no questions is extremely helpful in testing: [it's actually an important part of how I write test plans](/blog/posts/how-i-write-test-plans-for-new-functionality/). Writing tests that focus on yes-or-no questions has also been very helpful: if I can create a step definition that handles both *it should* and *it should not*, I get functionality to execute two different steps (one for *it should* and one for *it should not*) for the price of one. The more assertion steps a framework makes use of, the more I find this strategy pays off.

The main value Cucumber provides is to run code that defines the method portion of a step definition with a matching pattern that matches text is has encountered: if it encounters text it has a matching pattern for, it will run associated with that matching pattern. At the same time, something valuable that Cucumber does is allow software engineers to design step definitions in such a way that they capture parameters (i.e. variable content) passed as substrings within a particular step.

For example, at this point in code we will use the step definition's matching pattern to capture a substring that answers that defines whether we should evaluate for it *should* or *it should not*. In addition, I created the [`Expectation`](https://github.com/trevorwagner/spiegel-junit-med/blob/768ccd3d3a9a052ed741f9cd996cb9c9d7213bdd/src/main/java/io/twagner/spiegel/cucumber/glue/support/languages/en/Expectation.java) class to handle this. Expectation takes the strings "should" and "should not" as the argument to its constructor (otherwise throw an error so that we can fail fast). In case of regression, I define [tests against Expectation here](https://github.com/trevorwagner/spiegel-junit-med/blob/2eb6fcb9b94a70ca6de3dc516d61fc1a77a5422a/src/test/java/unit/io/twagner/spiegel/cucumber/glue/support/languages/en/ExpectationTest.java).

This, by the way, is a pattern I've picked up in my experiences. It isn't something I came up with myself. It has proven handy, though.

## Cucumber Scenarios/ Feature Files

Now that after all this work we have a framework that will support the tests we write, let's write some tests to go with the framework.

To be clear I don't always write tests last. As I can recall, I actually normally write Cucumber scenarios somewhat in tandem with step definitions. I also have a tendency to outline the sorts of Cucumber steps I would like definitions for and how I would like the language to look either before I start or as I go along. Being deliberate about this gives me an opportunity to think about whether or not it makes sense to capture certain substrings or how I'm trying to describe the system under test. I need to be able to use my language skills alongside my programming- and testing skills. What am I actually trying to do here: am I trying to boundary test? If I capture that value, I can use it later. What if we decide to extend coverage later: does the design I'm using seem open to that?

In essence this part is a creative process that depends on a number of factors. If I understand what I'm trying to test, the framework I'm using to test it, and how I put the two together in order to be able to define the tests I'd like to run, I'm off to a good start.

The Cucumber scenarios I wrote can be found in [both feature files I store in this folder](https://github.com/trevorwagner/spiegel-junit-med/tree/2f2ce3175bea3d518b42f1d02d7bde142d525b48/src/main/resources/features/duckduckgo).

At the same time, [hopefully I wrote a test plan](/blog/posts/how-i-write-test-plans-for-new-functionality/). A test plan is a good investment in not getting lost as I discover new things. The inspection checklist sort of functions like a to-do list at this point.

## Conclusion

My aim here was to reach a little beyond what I wrote to discuss why I wrote it. There is definitely more than one option to write a framework, and when planning a framework, I've found it pays to be clear on what those options are and to be able to compare and contrast them, both in terms of advantages and disadvantages. That's sort of Software Design 101, but unless it's clear which problems the author is trying to solve, it might not be clear how fundamental the design decisions they made were.

I believe in approaching test frameworks as a first-class software solution responsible for exercising and evaluating another piece of software. Within that, usability and general good architecture are as important as the ability to test something now. There is a lot of thought that goes into identifying the questions to ask in order to deliver to this standard, as well as how to go about finding answers. My other hope here is that this can serve as a starting point to discuss how I approach some of the questions here as well as the answers.