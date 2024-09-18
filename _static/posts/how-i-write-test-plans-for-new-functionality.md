---
title: "How I Write Test Plans for New Functionality"
publishDate: "2023-06-24T22:14:00-05:00"
coverPhoto: "glenn-carstens-peters-RLw-UC03Gwc-unsplash"
draft: false

---

Test plans are an invaluable tool for Quality Engineers. For me, they've helped to structure the work I am doing and provide me with a path to stick with as I test. Any time we find something unexpected in testing, it can be easy to start reevaluating and reframing any plan of attack for moving forward based on the new information. In essence, then: if test execution can be expected to produce new information that possibly also produces churn, a test plan can be a valuable tool to help limit that churn. As I understand it, it's generally common knowledge that this is table stakes for test planning.

Beyond limiting churn within my personal use, the test plans I write have helped me communicate clearly to nearly anybody in the organization I was working within what exactly I expected to get out of testing and (once testing was completed) what I actually got. Even further beyond this, they served as an instrument to effectively shift quality left on teams I've worked with by serving to test the understandings held by software engineers and product owners by listing inquiries related to the behaviors I expected to evaluate in the finished product. [I explain more about this in a future post](/blog/posts/making-acceptance-testing-as-boring-as-possible-how-a-team-moved-analysis-and-quality-assurance-left/).

I've used roughly the same general approach to writing test plans since 2010. The approach I use seems to have worked well for tests I've needed to execute as well as (both manual and automated tests) I've assigned to others to execute. Because this approach connect what gets tested to an understanding of why it should be tested, test plans I've written in this manner have also helped serve as documentation of what in essence was tested and why, so that either I or somebody else could review my test plans later on and get an understanding of how we approached acceptance- and regression testing when we first developed the functionality.

In this post, I'll walk through a little how I approach writing test plans and how the methodology I use relates to what it is I understand I'm trying to test/ test for.

## Envision an Inspection Checklist

Wherever I can, I try to define test plans I write in terms obtaining yes-or-no answers related to stakeholder concerns: yes is a pass, and no is a fail. I use this to build a checklist of questions that need to be answered in order to complete inspection. So from the beginning I start with a simple go/ no-go for any question of the value delivered by the system under test.

For anybody who's ever actually executed tests, hopefully the bell in your mind has alerted you to the reality that tests don't always return yes or no when executed. Don't worry: I hear the bell, too. Despite this, though, yes/no is still a good place to start. Either an API will return HTTP 200 (or the expected response code -- whatever that may be) or it won't. Either the login screen will allow access to the system (given specific input) or it won't. If you can focus your inquiries questions limited to yes/ no answers (and if you can focus them to the sort of evidence that you can gather to arrive at that answer), then you are on the right track.

For test results that are a little more nuanced than pass/ fail, I actually configure my test plans to account for six different outcomes:

- **N/A:** The inquiry is not/ no longer relevant to the evaluation the test plan is part of.
- **Pass:** The functionality behaved as expected.
- **Issues:** The functionality generally behaved as expected, but there were minor hiccups (likely not something that would return a "no" answer to the inquiry).
- **Fail:** The functionality did not behave as expected at all.
- **Unable to Test:** Something blocked full evaluation of the functionality.
- **Testing Incomplete:** For some reason other than a functional blocker, the tester was not able to complete testing of the functionality targeted by the inquiry. For example: the tester skipped the test in the current run.

So for anybody keeping track here: yes-or-no question, six potential outcomes.

The order here is important when using column summaries in [OmniOutliner](https://www.omnigroup.com/omnioutliner/), which is what I use to compose test plans. This might be a good topic for a future post.

### Not Every Question Boils Down to a Yes-or-No Answer on Its Own

Sometimes there are cases or specific behaviors that might introduce complexity to answering a specific question. For example, some questions present variations in the functionality. Maybe the behavior that's the subject of a question depends on other functionality, or maybe there are variations on how a behavior on its own can be evaluated to arrive at a yes-or-no answer to in response to a question. I'll generally add these cases as sub-points (each allowing for recording any of the statuses I list above) to the original question.

Each of these sub-points, though, should trace back to the inquiry developed within a top-level question, because they support responding to stakeholder concerns that any question posed within the test plan is expected to connect to. More about this below.

Now that I have a list of questions, and I have a limited lists of outcomes for the testing that will seek to answer each question, the next step is to find questions that I will use within this framework to attempt to show that the system under test is doing what we expect it to.

## Develop a List of Questions in Support of Stakeholder Concerns

Questions are a great place to start. Even if I'm not sure how testing for a new feature might fit together, I can at least ask a question. Generally for me, one question usually leads to more questions.

The inspection checklist I develop tends to conform to a general model I use (however unintentionally) to organize questions that will be asked to support a conclusion that the functionality under development is ready to ship. [I explain more about this in a future post](/blog/posts/three-rings-a-simple-model-for-test-planning/), but for now I'll outline my primary reasoning below.

Let's say you work for a software company. The software you write is important to customers of the software company. It's also important to Support: they are tasked with assisting customers either understand how to use the functionality, assisting them in finding workarounds for issues, or with documenting and escalating issues in shipping releases of software. Salespeople are generally responsible for leveraging the value the functionality provides to close sales. The list goes on with Sales Engineers, Deployment Engineers, Legal, Marketing, and eventually executive leadership. Also, you can't forget Software Engineers, both on any development team/s you're currently embedded with and elsewhere within the development organization. Everybody has a role at the software company related to the software that the test plan currently being developed seeks to examine, and for each of those stakeholders, depending on what it seems like the perspective of each stakeholder might be, their definition of quality might be slightly different, even if they share similar concerns informing what quality might look like.

When I write test plans, I ask questions I imagine any of these stakeholders might ask me about it. Actually, to be more accurate: I imagine I'm reporting to the sorts of stakeholders listed above that any of the questions listed above have been answered and that, now we have answers, it seems like the functionality under development is ready for release. If I reported this, I imagine the sorts of questions I'd be asked by any of the stakeholders listed above. I do my best to condense all of that into a limited set of questions.

There is actually a model I use to organize stakeholder concerns. I will outline that in more detail in another post.

### Concerns Related to Essential Functionality

Let's say the software you are developing is a toggle that sets status to ON and OFF. Actually, let's get a little more concrete and say it's literally a light switch. To test essential functionality I'd pose two questions in my test plan:

- *Q: When a user flips the switch to the `ON` position, does it enable the thing (like a light bulb) that the switch is connected to?*
- *Q: When a user flips the switch to the `OFF` position, does it disable the thing (again: like a light bulb) that the switch is connected to?*

Notice how these questions connect stakeholder concerns to a focused yes/ no answer that will be provided by the system under test. If it doesn't do these things, it's not a toggle.

This is pretty simple on its own: it outlines the concerns we expect the toggle to support, and it will most likely be relatable to stakeholders at any level.

### Concerns Related to Use Cases

Once I've established use cases that cover essential functionality, I generally expand planning to include inquiries related to use cases. This tends to be a little more open-ended than questions posed against essential functionality: any way users can be expected to attempt to use the functionality under test, and however the functionality under test is open to use, that presents opportunities for use cases. Those use cases can generally be related to stakeholder concerns.

As I plan testing, I usually find questions related to use cases challenge essential functionality, because they generally incorporate essential functionality without targeting it directly. So you say the speakers in your stereo system have a lot of drive: how well do they do their job if the user turns the stereo all the way up? Do they stay in one piece, or do they blow out?

### Concerns Related to Regression Scenarios

The way the functionality under test is implemented, it might have an impact on the viability of functionality implemented previously. Everybody has missed functional regressions before: they can either degrade existing functionality or knock it offline completely.

There are naturally going to be stakeholder concerns related to this, too. If existing functionality delivers value, then that value should be protected somehow by evaluating it to confirm that it still works.

Concerns Related to Complications in Functionality

There might be external systems that the functionality under development interacts with somehow. An easy example is an API that gives your functionality access to an external system.

At the same time, though, what if the software you're testing imports scans directly from a TWAIN scanner: this isn't as common now, but it used to be (I actually tested software at one point that did this). On Macs, TWAIN scanners did not play nicely prior to the ImageKit API: they loved to crash custom software that imported from them directly. Also, sometimes imported pages did not collate as expected. Because TWAIN in practice was more of a convention and less of a standard, it gave driver- and software developers a lot of room to develop custom behaviors that made it difficult for custom software to import from them directly. This led to a lot of additional questions being added to test plans that otherwise seemed like they should have been straightforward.

## Consider Giving the Questions Structure

This is a tough one to explain, because I believe it's pretty subjective. When I write test plans, the questions the test plans pose are first class citizens: they link evaluation to stakeholder concerns by posing yes-or-no lines of inquiry related to value. As I assemble test plans, I sometimes end up with a long list of questions that don't really have structure: maybe five questions about this, seven questions about that, then another eight about something else. For anybody not doing the math I now have 20 questions. All in a row, that's sort of monotonous, and whenever I've tested (whether it's in a print shop or software QA), monotony makes it easy to miss things. It also makes it a challenge to break testing up if the work to execute the test plan is divided among colleagues.

The format I use to write test plans as an inspection checklist is an outline. What I will do, then, as I outline, is take a step back once I have the 20 questions and see if the 5-7-8 grouping seems like a valid structure to describe overall what's going on in the story or whether there's maybe another grouping that might help break up the monotony and provide main sections (or subsections) to group my tests into. Then I name the sections and subsections.

Naming the parts of the structure can sometimes reveal additional avenues for testing. For example, if the functionality being implemented is a bicycle drivetrain, naming the chainring, the chain, and the cassette individually may reveal functional areas that weren't distinct before, especially if all the user story talks about is the drivetrain and how the drivetrain will help the rider get the bicycle moving.

Again, it's subjective. The way I decide to structure questions is subjective, the way I ultimately divide and structure them is subjective, and what I do with section headers once I've written them is subjective. What I've found, though, is that if I can find something within all of this that seems concrete that I can use to structure how I plan on approaching testing, that helps me understand more clearly what's important within what I plan on testing. If I can make that clear for myself, then hopefully that's also a step in the right direction to make it clear to others.

## Ask Whether there are Any Other Concerns That Haven't Been Considered

Once I've listed as much as I can, I start quizzing myself whether I've potentially missed anything. Using a turn of phrase that's hopefully familiar to anybody reading this that's familiar with engineering: now that I've listed all of my knowns, I'm interested in discovering potential unknowns. As I test, I leave the door open to modifying my test plan, but the more complete a test plan I can assemble on the front end, the less discoveries I find that I and the team I'm working with likely need to accommodate later on. Before I mark test planning complete, though, I generally spend some time asking the part of my mind that comes up with ideas whether I have any other ideas, then I compare those ideas to what I already have written down.

If I've found something new, it's often a good opportunity to restate my assumptions and ask whether it seems like the structure I've provided within my test plan likely misses some functional area that's important to stakeholders. If it's not something new, no problem: I have a place to write it down.

If I can go for long enough that I feel confident that I'm not raising any concerns that I haven't covered already, then I'm good to go. This usually depends on how complex the functionality I'm testing is and the level of risk it seems like there might be in missing something. For some functionality I've idled in this stage for as long as days; I've also waited an hour. Nights and weekends generally help with this.

## Conclusion

A long time ago I had a teacher who suggested that any time we read a text, we should first take inventory of what we expect to get from the text, then read the text, then compare what we expected to get from the text to what we actually got.

I am generally not much of a fan of process for the sake of process, but the same way I've found this suggestion (incredibly) valuable for reading comprehension, I've found it equally as valuable for test planning. On top of this, what I've found is that the clearer I can be about what I plan on testing and why that testing is important, the clearer I understand what stakeholders can expect to get from the new functionality I am tasked with evaluating and how I might best address those expectations in the test plans I write.

As I write test plans, the inspection checklist I outline in terms of yes-or-no questions helps focus inquiries into these expectations: either it will or it won't, and here's why that's important. To restate this with slightly different words: *[the why](https://www.youtube.com/watch?v=u4ZoJKF_VuA#t=2m34s) is an important part of testing (at any level), and part of the value in the method I outline here for developing test plans connects the why to the how and the what*. And by rendering questions in terms of stakeholder concerns, I've found that I can make it clear to anybody in the organization not just what I'm testing but why I'm testing it. Everything traces back to stakeholder concerns (without which I don't believe there would be such a thing as quality), and the test plans organize not just execution but also the information they intend to extract in terms of those concerns.