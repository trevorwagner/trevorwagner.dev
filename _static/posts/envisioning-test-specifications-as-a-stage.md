---
title: "Test Code Readability: Envisioning Test Specifications as a Stage"
publishDate: "2023-10-17T13:51:00-05:00"
coverPhoto: "https://static.trevorwagner.dev/images/mark-williams-9bNmhMKQM1Q-unsplash/1200x800.jpg"
thumbnail: "https://static.trevorwagner.dev/images/mark-williams-9bNmhMKQM1Q-unsplash/300x200.jpg"
draft: false

---

It's once the lights go down that the exhibition begins.  That event that you bought tickets for, that the audience has (hopefully in an orderly fashion) filed into the venue and taken their seats for (if there are seats) is about to start.  Once the house lights dim, the stage lights illuminate the area in front of the audience where the exhibition to which the audience has committed to bearing witness will begin to unfold.  

Test code and test support code that is easy to read presents several benefits including being:
rot
- Easier to organize, move, and reorganize.
- Easier to troubleshoot and debug.
- Easier to quarantine and remove from quarantine.
- Easier to assess coverage or associate coverage with production functionality.
- More accessible as documentation of the system under test.

My experience has been that tests, test code, and test support code that invested in readability early on tend to experience better return on investment and lower maintenance than those that did not.  In essence: when we cut corners on test code readability, it seems like the best we can expect to produce is a lot of waste paper.

Despite this, my experience has also been that many software engineers (including some of the best I've met) seem to struggle occasionally to find ways to make test code simple and readable.  The best explanation I can think of seems to make sense: if your focus is writing (and optimizing) something like a generic DAL for RDBMS, client/ server WebSocket connections, a complex JavaScript queueing service, or single-page Web apps that make extensive use of dependency injection, it might not seem evident to how go about testing (especially a system you wrote) if the best you have to work with is an IDE and an imperative to test.  A [recent post to The New Stack](https://thenewstack.io/unit-tests-are-overrated-rethinking-testing-strategies/) seems to support my reasoning here.

By the way, that's a situation where a good QA Automation Engineer (or an SDET; out of convenience we tend to answer to many names) might be helpful.

When I approach test specifications (like test methods or Gherkin scenarios) either to write the or to read them, I often find myself looking at them in within a specific frame.  The assertion statement and any associated action/ retrieval of a result generally take center stage.  Test setup and teardown and test data management to me look a lot like a stage crew managing the production behind the scenes.  The test method name (or scenario title) serves as a poster advertising the exhibition.  At first these comparisons sort of pointed themselves out for me (wasn't looking for a model); now they serve as a sort of guide.

I have personally gotten a lot of value out of looking at test specifications like this (especially for test code readability) and organizing my own code using this analogy as a model.  My aim with this post is to share what I see and help explain what I see within it that might be illustrative to others.

Fair warning that I'm going to lean heavily here on [Arrange-Act-Assert](https://www.linkedin.com/pulse/three-building-blocks-great-test-suite-john-ferguson-smart/?trk=articles_directory).

Also, a quick note that this post probably isn't for everybody (especially where I use a lot of non-code to talk about writing code), and it's definitely not conventional for a post related to QA Automation. With this in mind, though, I figured I'd share anyway.  Again, my hope here is that this is potentially illustrative to others.

## The Assertion Statement: The Moment of Truth for Expectations

Somewhere, a well-written test specification tasks itself with verifying that the results expected to have been retrieved from the system under test are the same as the results actually retrieved.  In the sort of moment of truth that the assertion statement presents, the test will pass if what actually happens matches what we expect to happen; otherwise (if it does not match), the test should fail on some sort of assertion error.

Something very similar happens at a circus and frequently during magic shows when the production announces a high-stakes stunt, then completes that stunt successfully.  The lion tamer, the trapeze act, and even the illusion of sawing a person in half seem like they shouldn't be possible, and in the audience we generally react sort of viscerally once these stunts are announced (because we understand how dangerous the stunt might normally be).  These are generally moments of great suspense and tension driven by two different sets of expectations (the lofty expectation that was announced and the grim expectations the audience generally holds as common sense), where the ringmaster or magician announce the stunt and stage lights are dimmed other than a spotlight (or similar) focused on the stunt itself.

In practice I find there is sometimes dissent as to whether assertion statements are actually necessary.  I disagree, but it seems like an extended discussion deserves its own post.  Maybe someday.

When I read- or write a test specification, I try to maintain focus on the assertion statement first.  It's generally lower stakes (for example, a response to an HTTP call generally returns the expected response code or it doesn't) than a circus or a magic show, but much the same way as with the above it's worth focusing attention on.  Generally I've found it helps the most if it is (on its own or paired with the action) the main point of interest within the test, both what the test builds up to and the point where one trapeze artists catches the other (no net) — or possibly not.  The only way to know is to watch.

## The Action and its Aftermath: A Turning Point That Leaves The Results Exposed

Before an automated test can compare results within an assertion statement, it needs to retrieve results first, which generally also requires triggering some action that exercises the system under test.  Somehow, test code needs to exposes data (extracted from the system under test, and the results are the product of some interaction with the system) and evaluate it.  At the point that a result has been exposed/ produced, the rest of the test's activity generally plays out within the test: by the time data has been extracted for comparison, test code shouldn't generally be any need to to interact with the system under test going forward.

Frequently in literature and drama, there's a critical point where a main character commits to a path from which there is no turning back.  This moment leaves the character exposed to the world around him/ her/ them and marks a point that the character's ultimate success or failure will connect back to.  In order for Neo in [The Matrix](https://www.warnerbros.com/movies/matrix) to save his friends (and eventually himself) by challenging the machines, he first needs to take the red pill (and by doing so trust one of the people he would later attempt to save).  The tragedy of King Lear plays out following the title character's dissolution of critical relationships upon retiring from kingship (in favor of relationships that flatter him the most).  In the Odyssey, the only way Odysseus could return home was to leave Troy (although Odysseus did this without first making a sacrifice to the true inspiration for the Trojan Horse).

The stage provides a great setting that can be used to focus audience attention on the importance of the the moment: as long as the stage has the attention of the audience, the isolation of the stage itself can be made a setting for the moment.  Depending on the venue and the production, this might be accomplished with something like creative lighting choices, absence of other characters onstage, or a change in sound effects.  Maybe even innovative computerized special effects and a giant mechanical claw drawing the main character into a bright light.

It might worth noting briefly that, within a test, action and retrieval might be the same action (in essence, the same statement in code), or they might be separate.  Also, it may be that what a specification means to evaluate relates to default state (at which point no need to trigger an event).  

Where a test specification does call for evaluating the results of an action, it's important to understand how that action relates to the assertion statement and how it produces the result that gets compared within the assertion. It might also help to make it clear how the the action relates to any data/ state management undertaken thus far within the test method.  A lot of the work (if any) needed to make this clear comes from formatting, method- and variable naming, and keeping the rest of the test specification tidy.  More of this last part below.

## Arranging Props and Background: Test Setup and Teardown, Data/ State Management

In order to present a situation where the system under test can be exercised (and a result can be extracted), sometimes we need a system (or component, or mock) configured, we need data generated, or something else to configure the system state needed to execute the test.  This can be a lot of work, and the more low-level work you do within a test specification, the more noise this ultimately produces that competes with signal (the assertion statement and the action that produces the actual result).

Some stage productions (not all, but some) benefit from setups or changes (things like set changes, scene changes, costume changes) during runtime.  Where it seems like they do, the productions generally also benefit from planning the setups or changes so that they limit interruption of the production for the audience.  There are quite a few strategies available to make this seem seamless, including moving sets or backgrounds between scenes, dimming the stage lights, or even hiding musicians or backup dancers under the stage or in set pieces.  Because the show must go on, care should be taken to make sure that moving the production along does not stop the show unnecessarily.  

Within a test specification, if I know what my assertion statement is, and I know what the action will be that produces a test result, then I can generally also take it for granted that everything else works in support of those two things.  Test setup arranges the scenery for the action statement.  Maybe it introduces some auxiliary characters.  However much any of this helps, it also pays to be judicious with it.

Otherwise, my experience has been that you generally want test support code behind the scenes, in support of the magic onstage.  Lifecycle hooks provided by the test runner are a boon here.  Making judicious use of [Object-Oriented programming principles](https://www.linkedin.com/pulse/4-pillars-object-oriented-programming-pushkar-kumar/) and common design patterns (I personally try to use [Gang of Four patterns](https://www.linkedin.com/pulse/design-patterns-principles-high-level-view-fukizi-mcsd-mct-/?trk=pulse-article_more-articles_related-content-card) where I can) can help encapsulate functionality supporting the stage crew in classes and helper methods that are easy to share (as an author) and get familiar with (as a reader).  In the right situations, parameterized tests allow for expanded coverage using a common pattern. 

At the same time, though, I believe it's still vital for tests to quality their environments and, for example, fail fast if it encounters an issue that would otherwise prevent either the action or the assertion statement from doing their job (both in cases where everything is nominal and in cases where they are not) smoothly.  So here the comparison to a stage show breaks down a little.  Within test code, you want the stage crew to be ready in essence to pull a fire alarm in case of a problem setting up the stage.  

## Advertising the Exhibition: Using a Descriptive Specification Name/ Title

Naming a test method or a scenario presents a valuable opportunity to help readers (maybe even yourself later on) understand what the test does and why it's important. 

It's sort of like the sort of [flypost advertisements (also described as "wild posting")](https://www.google.com/search?sca_esv=573896841&q=wild+posting&tbm=isch) that were (and in some places still are) posted to advertise events in public areas.  Circus posters generally visualization of some subset of the acts included in the show, including elephants, trapeze artists, and magicians: in addition to providing something visually striking to sell the event, it also serves as a visual description of what the audience should expect.  Expect a circus with clowns and a high-wire act.  Expect a rap show with this rap artist.  Expect a comedy show with this comedian.

When I write tests, I try to add the title last; otherwise (if I've already added a generic placeholder like `it totally works`), I will rewrite the method name to attempt to make it clearer.  To do this I'll try to capture as much of the following information as possible:

What the expected result, behavior, or product of exercise is.

How the result to the action taken on the system under test (usually framed as "when," for example in Python: `def test_lights_turn_on_when_lightswitch_flipped_to_on():`).

Which functionality or component the action is taken on or exercised.

## Conclusion

In order to test software effectively, you actually need to present an exhibition of what the system under test can do and presenting that exhibition within an isolated space.  This is not much different from what happens in a play, a magic show, a circus, or many other types of productions presented on a stage.  

I've done my what I can here not just to make the analogy clear but to attempt to tie this into descriptions of how it might be possible to use the comparisons outlined here to improve test code readability.  Here's a brief summary of what we've covered:

- Make it clear **where the assertion statement is**, how expectations are defined, and **how the expected results are compared to the actual results**.  Train a spotlight on the high-wire act and so that the audience knows where to focus.
- Make it it clear **where and how the actual result is extracted from the system under test**.  For any moment where the system under test and its results are exposed to scrutiny (by the assertion statement), isolate that moment and make it easy to find.
- Find ways to **make test setup, teardown, and state management to participate unobtrusively within the test specification**.  At the same time you want the audience to notice that the scenery changed, it helps to utilize scene changes, lighting, and the stage crew to keep focus on the show itself.
- **Use descriptive specification methods and titles**, to make it clear what what is evaluated, how it is evaluated, and what the expected behavior is. 

In context, it's not a complete surprise that other other technology related to close examination also incorporate this sensibility into terminology describing their components.  With optical microscopes, for example, the platform that slides are clipped to while under examination is also referred to as a stage.

For tests that look like this (even if the example is a little unconcise), hopefully it's clear how to make them readable :

<pre><code class="language-javascript">
import { fixture } from 'system-under-test';
import * as chai from 'chai';

const expect = chai.expect;

describe(`it`, () => {
   it(`totally works`, () => {
      // arrange
      const expected = true;	

      // act
      const actual = fixture.returnResult();

      // assert
      expect(actual).to.equal(expected);
   });
})
</code></pre>

For anything much more complex than this, hopefully the extended analogy I've outlined here provides sense helps make test specifications you write easier to share and easier to read.