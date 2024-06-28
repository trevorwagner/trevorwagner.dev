---
title: "Understanding Test Automation Frameworks: What is a Test Automation Framework?"
publishDate: "2024-06-28T15:42:06-05:00"
coverPhoto: "https://static.trevorwagner.dev/images/trevor-wagner/bike/back-end/1200x799.jpg"
thumbnail: "https://static.trevorwagner.dev/images/trevor-wagner/bike/back-end/300x200.jpg"
draft: false

---

When we use the term _framework_ to describe tooling that we use to write, run, and debug automated tests, what exactly do we mean? For example, consider:

- **Is Cucumber a framework?** [Cucumber describes a class of natural-language-driven test runner](https://cucumber.io/), which runs test specifications defined by users as text (for which Cucumber then runs associated blocks of code in step definitions with matching patterns that match that text) rendered as steps in feature files. As is characteristic of any other test runner, Cucumber can be written to define and execute test specifications.
- **Is Selenium a framework?** [Selenium describes conventions for a type of UI automation library](https://www.selenium.dev/) that allows test code to access Web browsers (traditionally by way of a RESTful API). Selenium can be used to automate interaction with a Web UI.
- **Is Cypress a framework?** [Cypress is primarily an Electron application](https://www.cypress.io/) that facilitates direct interaction with a Web browser by means of launching the Web browser binary within Cypress/ the Cypress electron app. Cypress is used to write automated Web UI tests. Cypress also ships with an integrated test runner.
- **Is Playwright a framework?** [Playwright is (also) a browser automation library](https://playwright.dev/) that (much like Selenium) allows test code to interact with the browser by way of a connection. Playwright can be used automate interaction with a Web UI.
- **Is Appium a framework?** [Appium is a UI automation library for mobile applications](https://appium.io/). Much like with Selenium and Playwright, Appium facilitates communication with an already-running mobile app. Appium is used to automate interaction with a mobile App's UI.
- **Is Postman a framework?** [Postman (and the associated Newman) is an API test automation tool](https://www.postman.com/). Postman provides a UI that allows testers to define and execute tests that evaluate behaviors exhibited by API endpoints (for example, RESTful or SOAP endpoints that allow interaction via HTTP).

A reasonable answer to each of these questions seems to be _yes and no_. Each one is in essence a software framework: each provides a collection of tools (as described within certain definitions of a software framework: an _abstraction layer_) that can be used to build additional software by way of leveraging the original framework. In this regard, it might be more accurate to describe Postman as a _platform_ (the word it uses describes itself, anyway) or testing tool/ workbench and less of a framework.

With the exceptions of Cypress and certain distributions of Playwright (for example, the [@playwright/test](https://www.npmjs.com/package/@playwright/test) node package, which combines the standalone [playwright](https://www.npmjs.com/package/playwright) package with a selection of test runners), it seems less convincing to suggest that any of these is a self-contained _test automation framework_. As a type of software framework, test automation frameworks make it possible to define and execute automated test specifications and test suites (collections of specifications). This is primarily done using the APIs provided by the test runner and associated assertion libraries. Test support libraries generally provide additional functionality that facilitates things like interaction with the system under test and the ability to abstract low-level test operations code.

Much like any other software framework, **test automation frameworks allow for definition of new functionality (automated tests) as built on top of the underlying libraries**.

It used to be that test automation frameworks were generally fully custom (or, in some cases, purchased as a standalone solution from a software company). These days, some solutions (somewhat like those noted above) are made available as off-the-shelf automation frameworks or even SaaS solutions. More recently, some solutions have presented themselves as low-code or no-code solutions or AI testing tools.

In addition, many of the examples provided in the list above (and others) challenge the conventional boundary between what is a full framework and what might be usable as a component library within a full framework.

Much like with repairing an engine, tuning a bicycle, or working on a house, it pays to understand how the parts of a test automation framework fit together and work together in order to understand better how to write, read, and debug the automated tests that depend on it. In service of this, this post will serve as the landing page for a series that will attempt to do two things:

1. Make it clear how these parts function and relate to each other.
2. Make a strong case for sensible nomenclature around these parts.

## Posts in this Series: Understanding Test Automation Frameworks
Here are the posts envisioned for this series:

- [What is a Test Runner?](/blog/posts/understanding-test-automation-frameworks-what-is-a-test-runner/)
- What is an Assertion Library?
- What is Test Support Code?
- What is Test Reporting?

Although providing a definitive how-to for building a test automation framework will lie outside of the scope of this series, it might be worth noting code walkthroughs (like [this one](/blog/posts/code-walkthrough-simple-framework-running-ui-tests-with-cucumber-jvm-sprinboottest-and-selenium/)) and design overviews (like [this one](http://localhost/blog/posts/how-i-improved-testing-stability-and-reduced-test-runtime-by-90/)) are also available elsewhere on this blog and provide descriptions of how I have put the pieces together in the past to build custom frameworks in various languages.