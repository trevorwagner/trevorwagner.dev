---

title: "Understanding Test Automation Frameworks: What is a Test Runner?"
publishDate: "2024-06-13T14:25:24-05:00"
coverPhoto: "trevor-wagner/bike/link"
draft: false

---

At the most basic level, support to automate tests requires two things:

- a means of **defining the components of- and parameters for automated test runs**, including test specifications, test suites, test run settings, and test reporting.
- a means to **execute test runs they have been defined**.

**Test runners** are a special type of software library that satisfies both of these basic requirements. In essence a test runner will provide two APIs that satisfy the needs outlined above:

- A code-level API that can be used to define test specifications, test steps (operations generally defined as a functional subset or component to be used within one or more specifications), and/ or other operations that should be carried out in runtime.
- One or more external APIs that can be used to execute- and configure test runs.

The [moment of truth (where the magic either happens or it does not)](/blog/posts/envisioning-test-specifications-as-a-stage/) for automated tests is **test runtime**. Within test runtime, test specifications drive test runs: everything revolves around the ability to keep test specifications moving, to execute them as implemented, and to report on their results. Test runners provide a means of defining test specifications, determining how to link- or group them together (for example as a test suite), determining how to handle operations in support of specifications, steps, or test runs, and how to handle situations where specifications or other operations do not function as expected during test runtime. In essence, then, test runners help define the drivetrain of a test automation framework: they provide a means to rotate through test specifications at the same time they provide a means of initiating rotation.

Test runners are used to execute automated tests defined at any applicable (i.e. non-manual) level of the testing pyramid. As many are implemented, they tend to follow some general conventions that help make their operations accessible and predictable to anybody familiar with the conventions. This post will outline some of the most basic conventions.

## Test Runners Provide APIs Used to Execute Test Runs
As noted above, one of the general APIs a test runner provides allows for a user to begin execution of a test run. Most test runners actually provide two separate APIs that facilitate starting a test run: a **command-line API** and a **code-level API**.

### Command-Line API for Test Execution
Like with most user space processes, the execution of automated tests starts in the command line. If tests are run on a Continuous Integration server, the run is started from the command line. Debugger sessions in an IDE are generally started from the command line (even if inputs and outputs are accessed and represented within the UI). Test runs started in Terminal, cmd, and PowerShell are (for anybody potentially curious at this point) all started from the command line. Even if tests are executed using a task runner (like `npm run test`, `./gradlew test`, `make tests`, or something similar), the task names serve as aliases for executing the test runner as a program (somehow, even if via an interpreter like `node`) via the command line.

Regardless of whether a given command line call is executing the library directly or somehow indirectly (beyond the `node` example above, running code that then configures and invokes/ executes a test run from within general runtime), the execution of a test run needs to start somehow. One of the key things a test runner provides is an API that can be used to start execution from the command line.

### Code-Level API for Test Execution
Most test runners also provide classes and methods within code that can be used configure- and begin execution of a test run. For example, [Jasmine](https://jasmine.github.io/) allows defining a test run with JavaScript code that looks like this:

```javascript
import Jasmine from 'jasmine';

const jasmine = new Jasmine();
jasmine.addMatchingSpecFiles(['tests/**/*.spec.js']);

await jasmine.execute().then(() => {
  resolve();
});

```

This can be useful in a number of cases, even if it's likely not especially intuitive for beginners. For example, a configuration like this can be used either to encapsulate suite configurations or extend (for example, by way of passing custom configuration options via command-line arguments or environment variables) built-in support the runner offers for configuration. It can also potenitally be used to configure parallel test runs launched within a process executed with a single command.

## Test Runners Provide Code-Level APIs Used to Define Test Operations
If test runners help define the drivetrain for a test automation framework, test specifications are like links in a chain on a bicycle (or a motorcycle, or sometimes a scooter). Even if every test is potentially fairly unique, each specification is a relatively-standardized segment of code that can be used to define how tests operate. If needed they can (again: much like with a bicycle chain, within reason) be managed or rearranged.

With test runners that use code to define specifications, test specifications generally look like some kind of method (read: function). In pytest and unittest in python, these methods all incorporate the substring `test` in their name. In JUnit and TestNG, these methods use the runner's respective `@Test` annotation.

With test runners (like Cucumber and behave) that use natural language to define specifications, specifications are stored in text files formatted using Gherkin syntax. Test specifications generally have titles that start with the keyword `Scenario:` (unless they are parameterized, at which point they start with `Scenario Outline:`).

### Test/ Suite Lifecycle Hooks
In addition to allowing users to define test specifications, most runners also allow for defining operations that should occur before or after every single specification (or group of specifications) or before- or after a test run. This can be useful for maintaining state (for example, cleaning up data stored within the system under test or an auxiliary datastore somewhere) or taking action based on the exit status of a specification.

Most runners define these as methods using special names. Cucumber and behave provide two different forms of lifecycle hooks: one type defined in code and another (strictly for setup) for all scenarios in a file by using the keyword `Background:`. The big three JavaScript test runners (Jasmine, Mocha, and Jest) use methods with names including the substring `before` and `after`.

## Test Runners Report on The Results of Tests and Test Runs
In addition to executing test specifications as part of a test run, most test runners provide some sort of output reflecting both the current status and the final result of the test run. Where most test runners provide support for executing test runs from the command line, this will be printed to output in the command line as output of some sort.

Test runners can also be configured to save reports of test results to file, like [JUnit-style XML](https://github.com/testmoapp/junitxml). That will be out of scope for this post; this post will deal more specifically with the ways results are reflected during- and after test runtime.

### Current Status or Progress to Standard Output/ `stderr`
In addition to other output allowed to display in standard output (pytest, for example, requires special configuration to capture current output to standard output), many test runners will print the progress of the test run to standard output (and/ or standard error), including which test specifications have been run and what the result of each test was.

This can be valuable beyond monitoring test status in a terminal window or live CI log as a test run executes: with some runners it is possible to correlate log output printed to standard output with the name of the test being run.

### Test Run Result Affect Runner Exit Status
When test specifications run they either pass they don't. The most common way for a test specification to fail is by way of an assertion error, where an assertion statement (tasked with comparing the actual result extracted from the system under tests against the expected result defined within code for the test) throws an error upon detecting a mismatch. Specifications can also produce errors (generally distinct from failures) if they encounter an unexpected behavior distinct from a mismatch.

Regardless of whether the specification failure was the result of a test error or a test failure, a non-passing result generally occurs any time a test specification encounters an error or exception (as supported by the programming language tests are automated with) as the test specification executes. As an aside, [this can be used in service strategies to enforce test integrity and reduce overhead in automated testing](/blog/posts/making-the-most-of-throwing-errors/): if the state or status of a test specification varies from expectations when checked within something like an if statement, an error or exception thrown manually can help prevent a test that's effectively out of true from continuing to run. Because most programming langauges support including error messages with errors when they are thrown, this can also help reduce overhead when troubelshooting failing/ erroring tests.

If any test specification completes with a non-passing result, the associated test run fails. Once a test run completes, the test runner will generally return a result status to the command line: passing runs generally exit cleanly, and failed runs generally result in nonzero/ unsuccessful exit status.

A nonzero/ unsuccessful exit status from a runner fails the task in CI executing it (although many CI platforms are able to determine before the process exits whether tests appear to be failing or not).

## Test Runners Generally Provide Means of Configuration and Extension
One of the natural benefits of any automated test is the level of consistency a test runner provides to execute tests runs the same way every time. Most test runners provide support for configurations that make this consistency customizable and sharable (for example, via code used to invoke test runs either via the command-line API or the code-level API for test execution).

### Extension via Configuration
Most test runners allow configuration via command-line arguments. In addition to this, many also allow configuration by way of configuration files. Some actually require a configuration file in order to start executing a test run: TestNG, for example, requires `TestNG.xml` to be present in order to begin executing tests.

In addiiton, runners that allow for execution by way of a code-level API generally also provide support within the same API to configure a test run.

### Extension via Code
Some test runners also allow subclassing or overriding portions of their APIs (as supported by the programming language they are implemented) to adapt and add behaviors to meet consumer needs.

## Conclusion
To anybody familiar, there is (of course) much more to test runners than what's outlined in this post. Depending on the runner, it may provide functionality that supports parameterizing tests, [nesting/ collating test methods](/blog/posts/collating-test-methods-to-limit-trips-to-external-systems-in-automated-tests/), executing tests in parallel, specifying a subset of tests (within files located at the specified file path to include- or exclude from test runtime), defining test fixtures to persist between specifications, or something else. Some test runners (like Jasmine and Jest -- both for JavaScript) provide integrated assertion APIs (distinct from standalone assertion libraries like [Chai](https://www.chaijs.com/) -- also for JavaScript). The list goes on, especially with runners like pytest or (regardless of the language-specific implementation) Cucumber.

For anybody unfamiliar, though, hopefully this provides a frame of reference for what a test runner does. Even if the objective for reading this post was to get a sense of what a specific test runner might be doing, hopefully this provides some context (beyond the documentation for that test runner, which should be essential reading) in terms of what test runners do conventionally.

In the end everything comes back to the chain (or maybe chains, if run in parallel, and regardless of whether tests are run at random or in the same sequence every time) of test specifications and/ or steps used both to define test runtime and drive test runtime. When building- or debugging a framework (much like working on a bicycle), additional functionality used in tests work either inside- or outside of the scope of the drivetrain that test runners help to define. Flow of control (and often object lifecycles for runtime featuring garbage collection) is handled by default within the scope of a link in the chain.