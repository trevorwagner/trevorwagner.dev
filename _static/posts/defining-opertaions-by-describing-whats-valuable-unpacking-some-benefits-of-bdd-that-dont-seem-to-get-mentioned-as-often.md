---

title: "Defining Operations by Describing What's Valuable: Unpacking Some Benefits of Text-Driven BDD Testing That Don't Seem to Get Mentioned as Often"
publishDate: "2024-01-24T15:10:00-06:00"
coverPhoto: "uniqsurface-C8F095Z9i5c-unsplash"
draft: false

---

Among test runners described as BDD test runners (relating to [Behavior-Driven Development](https://en.wikipedia.org/wiki/Behavior-driven_development)), there is a subset that use plaintext (instead of program code, or more specifically test code) to define and execute test scenarios. To be clear this is not to be confused with other BDD test runners (like Spock and what I call the "big three" JavaScript test runners: Jasmine, Mocha and Jest). Runners like Cucumber, behave, SpecFlow, and Gauge (apologies in advance if I've missed somebody's favorite) all operate using some sort of matching functionality, to associate a subset of custom code (generally provided within a step definition) to text the runner encounters within a plaintext file (such as a feature file). Test specifications are defined using lines of plaintext called steps; steps serve as building blocks to assemble test specifications.

I am personally very enthusiastic about text-driven BDD test runners, mainly because of the opportunities I'm aware they provide to access test automation (and automated testing) using [natural language](https://en.wikipedia.org/wiki/Natural_language) to define tests. With test runners like these, the same language we use as a tool to describe what's valuable about a piece of software (which, as experience time and again has shown me, helps to inform why we test software) is used as the primary tool to define what we test and how. Beyond this, the way these test runners make the language used to define tests modular, in essence promoting separability of test steps from the code that runs them and from each other. All of this has the potential to deliver enormous value in both testing and test automation.

Despite this, I've found that (for some reason) it tends to be a challenge to engage in conversations with development teams about the benefits of using text-driven BDD test runners. It seems like, if blogs and Websites conventionally define BDD test runners primarily as a **collaboration tool**, and if all the text serves to do is act as an **abstraction layer** on top of the code that actually does the work of testing, it's not clear why, as a tool, text-driven BDD test runners might be more valuable than a traditional runner like Jasmine, JUnit, or pytest. In some cases I've even gotten pushback due to what (if I'm correct) was the impression (however incorrect) that, with a BDD test runner, I meant to suggest that the team completely replace the way it currently operates with some definition of BDD.

I'd like to take a moment to outline (and unpack a little) some descriptions of what I see as highly valuable in text-driven BDD test runners that (as far as I can tell or have seen) doesn't seem to get mentioned often. From there I'd like to take another look at the conventional definition of what a text-driven BDD test runner is, from the perspective of how it functions.

As I do this, I plan on italicizing use of the words [define](https://en.wiktionary.org/wiki/define) and [describe](https://en.wiktionary.org/wiki/describe) occasionally within this post. In general, I believe it's valuable to bear in mind the distinction between these words (and the different activities they refer to). In this post specifically, though, I believe the difference between the two will help make clearer some of the points I mean to develop.

## What A Text-Driven BDD Test Specification Looks Like
If you wanted to write a simple end-to-end test against a workflow on a login screen using Gherkin (a line-oriented syntax common to text-driven BDD test runners), you could write a test specification/ scenario that looked like this:

```gherkin
Scenario: A login attempt with incorrect password and correct username is rejected by the login screen
   Given a user has visited the login screen
   And the user enters a value of "usernameWeKnowIsCorrect" to the Username field
   And the user enters a value of "passwordWeKnowIsIncorrect" to the Password field
   When when the user clicks the Login button
   Then the login screen should display an error message "Login Failed"
```

When the test runner (I wrote this as a [Cucumber](https://cucumber.io/) scenario) encounters this, it will iterate through each line and attempt to locate a step definition with a matching pattern that matches the line. If there's a match, it will run code paired with the matching pattern; otherwise most runners will throw an error (and some will print code it suggests to define a step definition that will match the step it encountered that resulted in an error).

Conventionally, text-driven BDD test runners also accept parameters for steps via something that resembles **string interpolation**: the step where the user enters a value to Username field can accept any string (including `usernameWeKnowIsCorrect`, passed as a substring within the step) to allow for one step to be used to cover a number of use scenarios.

## Unpacking the Benefits of Text-Driven BDD Testing
In the introduction (to anybody now trying to locate it: it's the second paragraph), I outline at a high level the sorts of value the general design of a text-driven BDD test runner presents in the ways it uses the association of language with code to define and execute automated tests:

- It makes test specifications writable (and readable) **in terms of natural language**.
- Because it **decouples** the definition of test specifications from the code that runs tests:
    - Steps (the lines of natural language used to define test specifications) are **separable from step definitions** (the programming code used to define test operations to associate with text matching the provided matching pattern).
    - Individual steps are **separable from one another**.

Below I provide brief descriptions of why each of these is valuable. Within the conclusion, we will revisit the definition of what a BDD test runner is. For now, brief descriptions are going to help us save time and space. I suspect, though, that it could be beneficial to cover any of these in greater depth at some point.

### It Renders Definitions of Test Specifications in Terms of Language (Not Just of Programming Code)
How would you describe a valuable workflow (ideally from the perspective of the consumer) using the same language anyone might expect to find in a newspaper or a magazine (or even possibly an email or an IM)?

Now, how would you go about _describing_ the same workflow using only test code?

The most obvious (hopefully) benefit of using a text-driven BDD test runner is that it uses natural language (and all of the benefits surrounding it) to _define_ test specifications by _describing_ valuable workflows. This goes beyond using domain-specific language (DSLs), which is what conventional definitions of BDD test runners as a collaboration tend to promote: instead it just uses language.

As [a software engineer myself](https://github.com/trevorwagner), I still find this comparatively more valuable, because it forces me to use natural language (tasked with rendering descriptions of what's valuable) the primary tool to define a test as opposed to the nonverbal constructions, patterns, and symbols used to write program code. In terms of what the language describes, it forces me to interact with value in terms of how I'd describe it instead of how I'd _define_ it (i.e. operationally).

### Its Use of Narrative Makes What's Valuable Relatable
Beyond use of language on its own, part of what makes text-driven BDD testing valuable is that it uses narrative to make descriptions of what's valuable relatable. The example I provide above is a self-contained story, with a beginning (or [inciting incident](https://www.studiobinder.com/blog/inciting-incident-examples/): `Given...`), a middle (I'd characterize this as a [point of no return](https://stevepavlina.com/blog/2020/10/the-point-of-no-return/): `When...`), and an end (here [a denouement](https://www.masterclass.com/articles/writing-101-what-is-denouement-learn-about-the-difference-between-denouement-and-epilogue-with-examples): `Then...`).

Even if we're not willing to [get especially technical or abstract about narrative](/blog/posts/envisioning-test-specifications-as-a-stage/) (which, if it helps, I believe is understandable), it should hopefully be clear who the scenario's main character (`a user`) is, where the action happens (`login screen`), and why the main character's goal (an attempted successful login) are all relatable; that relatability (as well as a clear understanding of why we expect the main character to fail) helps develop an understanding of value, which itself informs what's being tested and why.

### It Increases Accessibility of the Means to Test
This one gets mentioned occasionally, but it might be worth revisiting -- both in terms of language and narrative and in the distinction between description and definition being used within this post.

In essence text-driven BDD testing makes the definition of a test specification accessible to anybody who can understand a description of the workflow and [relate the workflow to both the composition of the system and user concerns](/blog/posts/how-i-write-test-plans-for-new-functionality/).

- Anybody who can read and write workflow _descriptions_ should be able to engage with defining tests without intimate knowledge how step definitions _define_ operations.
- Anybody engaged with functionality that _defines_ operations can (to a degree) disengage from the _descriptions_ of use cases in order to focus on how operations are defined by code.

Depending on how a team organizes, this may allow for specialization between team members who engage regularly with describing workflows and those who engage regularly with defining test operations. I have personally worked on a team like this, and I've worked on teams where I (as an SDET) was responsible for both.

### It Documents Supported Workflows
This one also gets mentioned occasionally, but along the same lines it might be worth revisiting briefly. Automated tests often provide a great opportunity to understand how the system under test runs under the hood: as a test net, they show how those who wrote the tests use functionality presented by the solution to attempt to confirm that the solution continues to exhibit valuable behaviors as expected. I know I've used this myself when engaging with code I'm not familiar with.

Within this, the relationship between definition and description is valuable, as well: the more closely or faithfully the text matched within a step definition _describes_ the functionality _defined_ within the associated code, the clearer any step using that definition will serve as documentation of the functionality it's tasked with testing.

As with any sort of abstraction (specifically [as a principle of Object-Oriented Programming](https://en.wikipedia.org/wiki/Abstraction_(computer_science))), it may still be necessary for any text step to dig into the code (the entry points to which lie just on the other side of the associated step definition) to get additional details on the implementation of a step or code supporting it.

### It Makes Scenario Generation Scriptable
If text-driven BDD test runners use plaintext to define test specifications, then anything that could potentially be used to generate the plaintext could also be used to generate working specifications; this includes code. Especially with a high volume of scenarios with functionality and tests that are highly modular, the benefits of automating the generation of tests presents opportunities for consistency and scalability with a single source of truth. It additionally presents the opportunity to render feature feels as easy to `diff`, in case of a number of hand-crafted scenarios or edits that (for whatever reason) end up not being easy to trace through with VCS.

At one point I actually scripted generation of a suite of thousands of Cucumber scenarios (mostly as scenario outlines) for functionality that was highly modular, mostly with the aim of making the suite easy to scale and modify if needed.

### It Makes Test Specifications/ Tested Workflows Portable
Because the association of natural language with program code separates test specifications from the steps and features that define test scenarios, they effectively decouple automated tests from the code that runs them. In addition to making step definitions reusable (which is a benefit of text-driven BDD test runners that does seem to get mentioned often), then, it also makes text steps portable to any framework with step definitions that support them. There are two ways I'm aware of that this separability can be useful:

- It makes it possible to take a set of feature files defining a set of workflows and rewrite the step definitions that define test operations (say, for example, that you have a set of e2e tests running against a RESTful API that you'd like to run against database queries at the integration level) to tests against the same workflows in a different context.
- Along the same lines, it also makes it possible to write tests against one part of a system (a Web UI, for example -- let's say [with a testing system like this, written in JavaScript](/blog/posts/how-i-improved-testing-stability-and-reduced-test-runtime-by-90/)) and write a second, separate framework that runs the same steps for a different part of the system (let's say the API, maybe written in Java or Python) to cover the system's response to the same workflows.

## Conclusion
Conventionally, the prevailing definition of what a BDD test runner seems to follow our understanding of what BDD is. Because this definition (again: conventionally) associates text with test code (and the code does the work of running the test), the text essentially functions as an **abstraction layer** for the code defining operations, and because the text is rendered in natural language (ideally leveraging DSLs), it also functions as a **collaboration tool**. This makes more sense for anybody who defines BDD in terms of [Test-Driven Development (TDD)](https://www.agilealliance.org/glossary/tdd/), which I don't plan on exploring in detail in this post.

These descriptions (however limited) seem to have been effectively promoted to definitions (however limiting) of what the subset of BDD test runners involved in text-driven testing do. Within this shorthand, any BDD test runner is (clearly) in essence just a collaboration tool and/ or an abstraction layer for test automation code. And when I look at the current top search results (for example, [this post by TestingXperts](https://www.testingxperts.com/blog/bdd-testing#Seven%20Benefits%20of%20BDD%20Testing%20that%20Ensure%20High%20Product%20Quality), [this post by Scriptworks](https://www.scriptworks.io/blog/bdd-testing/#the_benefits_of_bdd_testing), [this post by Agile Alliance](https://www.agilealliance.org/glossary/bdd/), and even [this post by BrowserStack](https://www.browserstack.com/guide/what-is-bdd-testing)), what I see are the same general high-level bullet points (collaboration tool and code abstraction) that seem to get reiterated in two-sentence comments on LinkedIn.

The same way I don't generally disagree fundamentally with these descriptions (they are fundamentally correct), I also don't disagree with benefits (like the reusability of step definitions) that tend to get listed more commonly. I do disagree, though, that what seems like the conventional definition serves a very comprehensive accounting of how text-driven BDD test runners are valuable (if not just usable) as a tool for testing and test automation. Some sources reach beyond the conventional definition. [SmartBear actually provides a comprehensive guide to BDD](https://smartbear.com/learn/automated-testing/is-bdd-right-for-you/) that goes the distance here (bonus points, by the way, for extensive use of the word "describe" and its cognates, which hopefully now can't be unseen). I find [this additional post by BrowserStack](https://www.browserstack.com/guide/benefits-of-test-management-and-bdd) helpful, as well.

That being said, there is a distinct set of benefits to using text-driven BDD test runners that doesn't seem to get mentioned often (if at all) in discussions of their merits. Put simply, runners of this type operate on a contract that looks like this:

- **Test specifications** are defined in terms of **natural language**. A tester writes a text _description_ of what should happen within a test specification (arrangement, action, and assertion), and that description is stored in a text file.
- When the **test runner/ execution engine** is run, it iterates through text it has been provided with and **executes code it can associate with that text** (for example, via matching patterns in step definitions). The associated code _defines_ operations to associate with the text.

This relationship presents a number of relatable functional- and non-functional benefits, for both testers and non-testers. It's what sets this subset of runners apart from other BDD-style runners (even runners like Robot Framework and Karate, which I might define comparatively as _keyword driven_ even if keywords are still text). The benefits of this relationship (regardless of whether they seem to get mentioned as often) inform why I, if I do suggest runners like these, make the suggestion. For a team or department potentially engaged in evaluating use of a text-driven BDD test runner, hopefully a more-comprehensive _description_ of the benefits can help fill in some of the gaps left by any _definitions_ that seem to get used more conventionally.