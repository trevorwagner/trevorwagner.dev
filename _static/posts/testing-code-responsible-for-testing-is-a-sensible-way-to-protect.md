---
title: "More than a Hot Take: Testing Code Responsible for Testing Is a Sensible Way to Protect against Risk, Safeguard Return on Investment"
publishDate: "2023-11-28T15:53:00-05:00"
coverPhoto: "c-d-x-8zKHg5JUp2U-unsplash"
draft: false

---

Imagine trying to chop down a tree with a dull axe. The bigger the tree, the better. For the metaphor implied here to work, though, the axe you use needs to be dull: with a dull axe you're probably not going to get very far for the effort.

To complicate things, imagine it's an axe that you've spent money for. In order to cut down the tree you are going to need to either sharpen the axe or go buy a new one. If you're lucky you could potentially also borrow an axe from somebody else, but you're already onsite and ready to get the job done. Either way, you are going to need to invest more into your main activity in order to ensure your toolset is suitable for the job. This lowers ROI and likely also produces waste. It likely also blocks other activities that depended on successfully chopping the tree down in the first place.

Along the same lines, code responsible for testing can (like any code) be expected to break unexpectedly. The code may start failing intermittently, which might cause tests to fail. Calls to external- or asynchronous systems may fail to resolve or return expected values in a timely manner. Code that returned one result might start returning another result. Or maybe an engineer "just adjusted one value" at a certain point in test support code or a custom assertion statement (in order to fix what seemed like a failing test) in a way that now changes functionality for other tests that depend on it. Regardless of how complex the code is that tests depend on,

A usable strategy to confirm that code continues to work as expected is to run automated tests against that code.

Here are four common arguments I've **encountered that software engineers use to suggest not to test code responsible for testing**:

1. Writing tests against test code is a sign that you're not confident in your original tests.
2. Testing code responsible for testing presents an unnecessary recursion that potentially leads to infinite recursion. If test code tests other test code, there's a chance you'll need to test the code responsible for that testing. If you keep going with this, you eventually end ups with test code all the way down.
3. The relationship between production functionality and test code keeps functionality for each in sync with the other. In essence: the same way that tests make sure production code works as expected, production code that functions as expected should ensure that tests continue to function as expected.
4. Testing test code is problematic because tests are flaky by nature anyway. If your ability to test production code relies on tests that are inherently flaky (as in: all tests are flaky), then you'll never test the production code because your test code will be stuck in build hell.

If it potentially helps to be clear early-on: I don't accept any of these arguments. At a formal level, the first is an appeal to flattery, the second is a slippery slope, the third (it seems to me) relies on a faulty comparison, and the fourth seems to me like an appeal to pity.

Within this post I will show why I disagree more fundamentally.

In fact (if not just my opinion), the reasoning supporting a valid counterargument (to these examples) is pretty simple:** if the imperative for testing is informed by a interest (followed through by investment) in gathering data to inform decisions related to fitness to ship, and if both the data gathered from testing and automation (itself) of testing tasks are understood to deliver high value, then the preservation of the integrity of any code defining (or supporting) testing activities should be given high priority**. Because developers and organizations depend on automated tests to make well-informed decisions, the integrity of the tests should be as valuable as the data the tests are expected to return, or else run the risk of challenging both return on investment, the data the investment is responsible for securing, and (at least) most other things that depend on it. The same way we task automated tests with helping to safeguard value presented by the system under test, we should be willing to use automated tests to safeguard the value this integrity provides.

In this post I'll outline my reasoning in support of this reasoning.

Also to be clear before we dive in, the argument I mean to develop here is related to why it makes sense to test -- not necessarily how much testing might be appropriate or where might be most appropriate to test. Where I believe it's likely most valuable to do this is test support code, mostly reusable code responsible for activities beyond setting and getting values from an object. I provide (a little) more info in a subheading (**Which Code Would be Valuable to Test**?) within the Conclusion section, below.

Automated Test Nets Are Tasked Returning Data That Is Accurate and Timely

In essence, we use automated tests to gather data on the value we can expect product to deliver. We use the data that automated tests return to inform decision-making and analysis related to the fitness of the system they evaluate (the system under test) for potential shipment, based how the data returned reflects the systems ability to deliver value as expected. However automated tests are used to gather the data used to inform decision-making, it's vital that this data be gathered in a manner that is accurate and timely.

In one example, when automated tests are run at frequency, they serve as what's referred to as a test net: in addition to returning data on the current status of behaviors, workflows, and functionality supported by the system under test, they also help determine whether a change has occurred since the last time tests were run, which can be used to inform a sort of forensic analysis to determine both when a breaking change to source code occurred and what the impact of the breaking change to current functionality (i.e. to value delivered by the system) might be.

In another example, suites of automated tests are used to define a set of functional requirements for shipment. Regression- or smoke test suites are used to evaluate the system under test and define a set of functional requirements that (as evidenced by a clean/ passing test run) the system must meet in order to be shipped or deployed. If a system fails these checks, the regression suite also provides data related to what is not working as expected.

Whatever we decide call a particular test run (or continuous set of runs), whatever business value we assign to the data we expect a test run to return, and whatever decisions we decide to make based on the data, the common thread is the clear relationship between the system under test, the tests that evaluate it, and the data returned as a result of the evaluation.

In essence this is **business intelligence**, and like any intelligence, its value is measured in its accuracy and timeliness. For this to happen, automated tests need to work as expected. If tests don't work as expected, the forensic information returned by a test net may not be either accurate or timely. If pre-shipment checks return false positives, they may flag a passing build unnecessarily. If they fail to catch non-conforming behaviors as expected it may result in an escape of unexpected behavior that was specifically identified as a blocker for shipment. None of this is either accurate nor timely.

# Automated Tests Require an Investment

However unintuitive it might seem initially (for anybody reading 100% literally here, that was light sarcasm), test code does not materialize out of thin air (if it helps, I don't mean this part sarcastically at all). Test automation requires experts of some sort to design and implement. They require hard resources (computers, drive space, electricity, servers, etc.) and soft resources (software, licenses, etc.) to use to in development. And above all of this, automated tests take time. None of this is free in software development, or even generally cheap.

Any software developer or organization that runs automated tests has already committed and followed through on the investments needed to make the above workable. And as outlined above, the accuracy and timeliness of data returned by tests depend on tests working as expected. So if tests don't return the data they are expected to consistently, they pose a challenge to return the investment the developer or organization has already followed through on to attempt to gather necessary data. Now not only is there a lack of data; that lack of data has (at least in the immediate sense of value testing returns for investment) become intrinsically more expensive than never having tried to gather it to begin with.

In addition to challenges to the intrinsic value of any affected automated tests (to implement automated tests), failure by any test automation presents two options to remediate, each of which presents its own set of risks and expenses that the data automated testing was expected to alleviate to begin with:

- Consider releasing with limited (if any) data. Either release without gathering additional data or gathering with the partial data they have been able to gather from tests that have run already.
- Delay general availability of the release candidate until sufficient alternative evaluation/ data gathering has taken place.

To return to the axe analogy developed within the introduction: not only does the axe that you've invested in not work as expected here; because the axe is dull you can't cut down the tree andyou need to re-adjust your plans related to cutting down the tree (including how to cut the tree down and anything for which cutting the tree down effectively blocks).

# The Risk of Code Breaking (Including Code Responsible for Testing) Follows Us Everywhere

One thing that is consistent about software is that it and its context can be expected to change. Either the code itself changes some subsystem (like nearby code, a dependency library, or even the operating system or hardware itself) changes. This includes browser automation libraries, libraries we use in test support code, and even test runners themselves. Sometimes changes to internally-developed test support code breaks tests.

If we're lucky we have an idea when code we're responsible for is going to break, based on things like announcements provided by the developers responsible for any libraries that our solution depends on. Sometimes we hear about it through social media, GitHub/ GitLab, or through other professional networks. Sometimes a test elsewhere gives us a clue. That's sometimes, and if we're lucky.

Other times, though, we're not as lucky. For example, even if the authors of the underlying libraries or subsystems tell you what they've changed, it may take some discovery to understand how upstream changes affect test code or even production code.

The same as with production code, test code is prone to breaking, including along the lines provided above. Evaluating code responsible for testing (including test support code) also provides data that can be used to make business decisions related to the value delivered by a specific build of the system under test. And although not every sort of integration with lower-level libraries or subsystems (browser automation libraries tend to be a good example) leave themselves open to evaluation, finding (or making, were possible) opportunities to gather data where possible can help to make data-driven determinations about the fitness of code responsible for testing to ship.

# Catching Issues in Test Code Early Can Help Protect against Unnecessary Complication When Troubleshooting

If we accept that any code (including code responsible for automated testing) is prone to breaking, then we also accept that some amount of troubleshooting and fixing will need to be undertaken to locate the root cause, as well as to propose, implement, and test a fix. The scope of any of this likely relates to the amount of our code used to define the solution. For example, if production code breaks, then the root cause likely has something to do with the system/s the production code implements or depends on. If we can catch that break before shipment (before it's deployed to production), generally that simplifies the amount of work that needs to happen to deliver a fix.

If code used in test automation breaks and we are able to catch it early, then the only system affected by the break is the automated test code. If the same code breaks while evaluating the system under test, we now potentially have at least two moving targets (the system under test and automated test code) that we need to troubleshoot in order to confirm why a test failed. This widens our search base, which likely complicates any efforts to deliver and confirm a fix.

What's more, automated testing is generally a serviceable way to execute regression testing in response to a fix. Lack of automated testing against code removes that option. Any fix to failing test code will likely need to be evaluated manually, if at all.

What's more: what if a fix to test code in one place results in tests failing in another? Depending on the complexity of your testing solution, this may be a possibility.

And again: this all challenges the ability of test code to deliver data that can be used to inform business decisions in a manner that is timely and accurate.

# Conclusion

Let's return to the example provided within the introduction, related to chopping a tree down with an axe discovered to be dull. Now that you're onsite and you've committed to chopping, imagine you passed on an opportunity to test whether the axe is dull earlier on: you've chosen not to check it before using it. Now that you've invested in chopping the tree down, you notice that you are not making as much progress as you might like, and you've applied resources (in addition to time, your energy and your hopes) to the attempt.

However strained this analogy may seem, the comparison it draws is apt. Any time you forego checking your equipment before attempting to use it, you leave yourself open to risk that the equipment will not work as expected when you need it to. On motorcycles this is why we use [T-CLOCS](https://msf-usa.org/documents/library/t-clocs-pre-ride-inspection-checklist/) for (relatively) simple pre-ride inspections. In mountain climbing, this is why it helps to have a partner check your setup. [Scuba divers do something similar](https://blog.padi.com/how-do-you-say-bwraf/) (although the acronym for this is more amusing to try to pronounce out loud than T-CLOCS).

If code responsible for testing (or supporting testing) fails at a time when it's expected to fulfill its business value, it creates waste that potentially blocks other activities and calls into question the usefulness (especially given the cost) of the tool to begin with. Any decision to forego checking tests before they are used accepts the risk of failure prior to any test run that depends on the untested code. And where it seems true that the system under test is complex and that the relationship between automated tests and the system under test is also complex, then it also seems true that the full impact of a failure in code responsible for testing will be made clear until it is fully assessed, which is part of what we task automated test code for in the first place.

In general, though, the reasoning in support of automating testing of code responsible for automated testing aligns pretty closely with the reasoning in support of automating testing any code in the first place. It takes time and resources to develop, we expect it to do its job, and when it doesn't do its job we're confronted with a lot of churn. Such a failure can be expected at the same sorts of points production code can be expected to fail -- the point is that sometimes you don't know until you see it fail, and depending on when you notice a failure, you may find yourself invested in a lot of extra work inadvertently. If you want to make the best of your opportunity, it's best to make sure your tooling for the job is sharp and capable before the work starts.

## Which Code Would Be Valuable to Test?

Much the same way as I do when evaluating production code, I tend to approach this in terms of value and risk. Personally I believe any utility code that supports testing that interacts with or modifies data beyond getting and setting a value on an object presents opportunity (thereby risk) for failure. Transforming data, building data structures, and interacting with external systems are all great examples. Use of an external library are good examples. I also believe it's worthwhile to test custom assertion statements. Really anything custom likely helpful to test, and testing helps protect against breaks resulting from upstream changes.

If I expect a utility method to get used a lot, I'll test it. The same with a factory class, [a library used to manage and validate test data](/blog/posts/design-overview-in-memory-generic-test-data-managment-in-javascript-using-lokijs/), or [a library used to create reusable API mocks](/posts/design-overview-reusable-mock-api-via-express-and-http-server/).

If it helps, here's a more-concrete example: at one point I wrote a builder class in Java (as test-support code) that assembled URLs (including query parameters) given values set on an instance of the class either through the constructor or via setter methods. I also wrote a set of helper methods that placed API calls to resolve human-readable names with unique record IDs for records stored within the system under test. On top of all of this I wrote a facade class (I called it a switchboard) that (much like a [manual switchboard operator](https://en.wikipedia.org/wiki/Switchboard_operator) accepted human-readable names for a destination, resolved IDs by placing API queries to the system under test, assembled the call for the caller (test code) to its destination (a URL containing the expected query parameters). The signature for the method that did this was Switchboard.placeCall(details). For reference, details was defined as a dictionary of key/ value pairs associating human-readable values with key names.

So in essence the switchboard solution relied on three units of code:

The builder class, responsible for building URLs given a set of values specified on an instance of the class.

The resolver class, which placed API calls to resolve IDs for human-readable resource names.

The switchboard class, which acted as a facade for the two (there was more to this, btw; for brevity this is all I'm providing), passed human-readable names to the resolver, and used the builder to build URLs using the resolved IDs.

Because the builder class did not interact with any external system on its own, I was able to test it and confirm that it built URLs as expected; that got me some coverage. Simulating API calls seemed like a poor use of time in the near term (and that was already handled by test code that evaluated the production API), so I didn't write tests for that. Similarly, I didn't test the switchboard e2e (between all three classes). If I had an opportunity to continue with that code, I would likely find a way to mock responses from the resolver class (to test the switchboard e2e). If I could mock API calls, that would likely be transferrable to other classes responsible for testing the production API.

**Bottom line: When it's time to test, you want your tests ready to go.** Whatever might make this confirmation easier to execute and potentially manage (especially given trade-offs in comparison with confirming manually or potentially investigating failures reactively), the better the ROI you'll likely experience from the resulting tests.