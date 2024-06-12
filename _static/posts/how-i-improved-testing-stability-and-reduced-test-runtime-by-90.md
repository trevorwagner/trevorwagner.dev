---
title: "How I Engineered a Solution to Improve UI Testing Stability and Reduce Test Runtime by 90%"
publishDate: "2023-08-11T14:50:00-05:00"
coverPhoto: "https://static.trevorwagner.dev/images/thomas-jarrand-K9GS65i36aQ-unsplash/1200x800.jpg"
thumbnail: "https://static.trevorwagner.dev/images/thomas-jarrand-K9GS65i36aQ-unsplash/300x200.jpg"
draft: false

---

Historically, evaluation of behaviors within a Web UI has been one of the most challenging and expensive things to automate testing for. There are a lot of reasons for this, including the anything related to the number of independent systems a test automator needs to interact with to get at the Web UI. Historically, automation code needed to interact with the browser (an independent closed system) in order to interact with the Web UI. In order to interact with the browser, automation code needs to interact with something like Selenium (which uses a RESTful API to facilitate interaction with the browser), Cypress (which runs an Electron app that facilitates  interaction with the browser), or more-recently Playwright (which presents a WebSocket connection that can be used to interact with a browser in a manner similar to Selenium but using a different client-side API) that also adds complexity to the relationship between any UI being tested and the code responsible for defining operations that should take place within the tests.

At the same time, in order to test the Web UI end-to-end (I'll refer to this form of testing as e2e) generally includes interacting with one- or more production systems designed to manage production data in production runtime. Conventionally in Web 2.0 applications these are the same independent systems that the Web UI interacts with in order to access data that it makes available to view or interact with. These production backends also make use of subsystems to enforce user access (or, once a user has access: access roles like CRUD permission sets) that require test code to administrate user sessions and user permissions.

To make this more readable casually: if I'm responsible for automating testing of a Web UI, and the only way I can get data into the system is by using a production backend that was designed to limit access to data, any ability to test the Web UI is constrained by the production backend -- whether those constraints are intentional or not.

If I'm a test automator focused on testing Web UI, this ends up making a lot of what seems like extra work. And after I've implemented testing, I can generally expect additional work when tests flake out due to concurrency issues (testing e2e against a configuration incorporating several different systems), data access issues, upstream changes in the backend (for example, if the company introduces CRUD permission sets in a system it did not exist within when testing was originally automated) in addition to any updates in the page UI itself.

Every complication makes the terrain for UI testing all the more precarious.

At one point in a previous life I was tasked with developing automated testing for a read-only page written in Angular. To sum the solution up generally I wrote a mock backend in JavaScript using (mostly) Express and LokiJS. In essence I replicated the production backend in testing of the front end to save on test execution time and to generally improve stability and debuggability.

In a couple recent posts I've written about a couple of the pieces that I used to solve this puzzle; in this post I'd like to talk about how I put the pieces together.

## Understanding the Problem

The Angular page was part of a larger 3-Tier Web app that looked like this:

- **Presentation Layer:** Angular.
- **Business Layer:** Java, serving two APIs (one RESTful and the other SOAPish).
- **Data Layer:** RDBMS (i.e. SQL).

Historically, to get around issues related to data setup and teardown, the organization that developed this 3-Tier system made extensive use of canned test data sets -- mainly sets of SQL data that were added to instances deployed to Staging once they were spun up. It was nearly impossible to get a deployment with no canned data.

In order to test behaviors on the page, I needed to make a choice: *accept the full stack as an external dependency for testing, or attempt to work around it.*  Ultimately I chose to work around the full stack, opting instead to write a system that managed test data independently of the business- and data layers, and to manage my own test data.

In production, the page displayed within an `<IFRAME>` element that was part of an outer page: the outer page provided view controls that made it possible to select (and search for) which record/s should display on an inner page (that displayed within the `<IFRAME>`). Selection within this UI presented a set of **display variables** that was passed to the inner page. Display variables were passed (as a JSON dictionary) to the inner page by way of an entity in JavaScript (as an [Observable](https://rxjs.dev/guide/observable)) that the inner page needed to subscribe to (using [RxJS](https://www.npmjs.com/package/rxjs)) in order to listen for events.

Certain behaviors on the page depended on the display variable selection state set when the page loads; others depended on the page responding to a change in display variable selection. To test this I needed support to set (and change) display variable selection and transfer the updated state to the page in a manner the page can subscribe to using roughly the same support code it used in production to subscribe to display variable state.

And in general, I had a couple standards that I wanted to meet in the work I did here, namely:

- I believe it's important that tests be easy to clean up.
- Testing code responsible for testing minimizes risk to test system functionality and anything that depends on It.
- Making test support code easily accessible is just as important as with test- and step Methods.
- Proactive test data hygiene generally pays itself off.

## General Design

My test runner for this project was [CucumberJS](https://www.npmjs.com/package/@cucumber/cucumber). It was my choice, mainly because I saw value in being able to frame tests against value in simple, human-readable terms. If you expect an OK button to display within a modal, write a step that declares the `OK button should display in the modal`. This could also provide additional value to make it possible to source manual user-acceptance testers (who were either not code savvy or who preferred not to write test code) to potentially write automated tests.

I chose to use Protractor instead of Cypress, which was also available at the time. Because Protractor was built on top of WebDriver, it provided support to test on more browsers (and in essence on more hardware) than Cypress did. This was important to the organization, because it supported some older browsers that Cypress did not. But in general I did what seemed like due diligence and developed a PMI chart to plot out pros and cons.

Mock API endpoints are served by way of [Express](https://www.npmjs.com/package/express). While investigating for design, I found that it's possible to start (and interact with) an instance of Express (more precisely: [http.Server](https://nodejs.org/api/http.html#class-httpserver), which Express is built on top of) during test runtime (in any JavaScript-based test runner I've tried with). What I built around Express was a set of wrappers that makes endpoints modular and allows for software engineers to define both endpoints and server configurations within test support code that lives separate from tests.

Cucumber actually presents two challenges when it comes to managing test data:

1. Cucumber steps on their own are generally **stateless**. You can save data within a variable scoped to a step method or a step class, but within the Cucumber step lifecycle once the instance of that step class has been cleaned up, any data saved on the step class gets cleaned up with it.
2. Cucumber uses simple substrings to refer to data in test runtime. So let's say you are using Cucumber to perform testing against search functionally, and you have records you've saved within a MySQL database as **record1** and **record2**, the best tool (arguably) available within a Cucumber step to recall either record is the substring used to define each record to begin with: **record1** and **record2**, to capture the relevant substring, and pass it as an argument to the associated step method. Let's say a test requires that I set a value on (or associate a set of values with) **record1**, then do something in the UI, then update **record1**, then review the UI again: how do I keep track of any data associated with **record1** if all I have to retrieve it by is a substring within a Cucumber step?

With this in mind, I needed some sort of test support system that could persist data outside of the scope of the current Cucumber step and help make generation and access of this data within Cucumber steps straightforward, as well as make it as intuitive as possible how to recall one record or another (especially if some workflows for the page I would be testing might require more than one record).

Big picture (as well as I can recall), everything fit together like this:

- Node invokes Angular using ng, which packages the app using webpack, which it then serves and starts a Web proxy for (the latter done using webpack-dev-server).
- Node (via Angular/ ng) starts Cucumber as the test runner for the test task.
- Within a lifecycle hook, Cucumber starts Protractor.
- Within a lifecycle hook, Cucumber starts the mock backend (HTTP and WS services via http.Server, for which HTTP routes had been defined using Express) within a Cucumber lifecycle hook.
- Cucumber sets test/ system state using a custom test data management system.
- Cucumber uses Protractor get the page (and interact with it) within a Web browser.
- In response to being rendered and interacted with, the page places requests (proxied by webpack-dev-server which had been configured by Angular when ng was first invoked) to the mock API.
- The mock API retrieves data from the test data management system and (after building a view with a view builder method) returns a view of the data back to the page.
- When a Cucumber scenario has completed, Cucumber uses an after lifecycle hook to iterate through LokiJS collections and remove any collection (the DAL will regenerate them as needed) matching a specific RegEx pattern.

The one thing I'm fuzzy on (if it helps: years later) is whether Cucumber bootstrapped Protractor or whether Protractor bootstrapped Cucumber. I believe it was the former.

In essence that's what everything looked like. Below I outline how I got there.

## I Wrote a Modular Framework that Serves Mock APIs Configured Using Express

It is possible to start an instance of  http.Server (which, again, Express is built on top of) in JavaScript test runtime. I actually published [an example of what this looks like to GitHub](https://github.com/trevorwagner/js-jasmine-run-express) not too long ago: if you manage the instance of http.Server (instead of starting Express) directly, it's possible to interact with any endpoints defined using Express between the point where the server was started and when the server was stopped. In the example I provide I start- and stop http.Server within lifecycle hooks provided by the test runner.

I wanted to find a way to leverage the ease of use (and portability using the Express [Router](https://expressjs.com/en/api.html#router) class) in setting up endpoints that Express provides while at the same time made facilitated use of a WebSocket endpoint and allowed interaction with the the underpinnings. So if all I wanted was a test mock (asap), I could do that with a minimum of code. But if I wanted to dig into the underpinnings (for example, to debug or experiment with something at a lower level), the system was designed in a way to make its underpinnings open to interaction, as well.

I describe my solution in greater detail in [Design Overview: Reusable Mock API with Modular Routing Using Express/ http.Server and optional WebSockets](/blog/posts/design-overview-reusable-mock-api-via-express-and-http-server/).

By the way: going forward I'll likely use Express to refer to anything also handled by `http.Server``. I do my best to distinguish the two clearly, but in conversation I tend to just describe this part of the solution as using "Express," so as not to get too deep into the weeds.

## I Wrote an In-Memory DAL to Manage- and Validate Test Data

Early on in design, I concluded that I needed a unified source of truth for system state -- both within the system under test and within the testing system (i.e. the test framework). If I stored everything centrally (in a single place) and I mapped the storage onto domain concepts, then I could change data for one person record, associate additional data to that person record, and rely on queries against that state to produce the API responses that the Angular page required.

Within the solution's use domain, there was a concept of people and a concept of calendars: once a person is assigned to the calendar, the person record becomes a record of another type. I needed a way to store records of each type, as well as to associate records of one type with the other.

I also recognized early on that any custom system I built to manage test data presented risk to the fidelity of that data. If the system stores state, what happens if that state changes unexpectedly between setting and getting the state? What happens if data gets weird and the tester ends up duplicating data (causing ambiguity in test data)?

I built a system to manage both of these things: test data itself and data fidelity. The system uses [LokiJS](https://github.com/techfort/LokiJS) for in-memory data backing; on top of this it uses a generic repository pattern. [I describe the solution in greater detail in this post](/blog/posts/design-overview-in-memory-generic-test-data-managment-in-javascript-using-lokijs/).

To associate records of one type with another (and inquire into which records of one type a record of another type was associated with), I built controller classes that leveraged the CRUD API built into the DAL. So to manage assignments of people to calendars, I might implement a controller class named `PersonCalendarAssignmentController`, with methods designed to create-, remove- and get status on an assignment relationship between a person record and a calendar record (again: stored within the test data management system).

## I (Eventually) Built View Builder Methods

Originally I wanted to save API responses directly within the database, which ended up being a terrible idea because it confused the concern of managing state with the concern of presenting data based on that state. Eventually I realized my mistake: I coupled test data management to the transmission of data to the system under test where I should have relied on (for test data management) was developing state as a function of domain concepts. In essence, this was bad [MVC design](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller). Lesson learned, but it took a minute to get there.

Fortunately my earlier attempt was salvageable. By utilizing view builder methods, I was able to convert the data stored as one format to data stored within another format. With view builders, data was prepared to transmit the way you might expect:

- The Express endpoint receives a request.
- The Express endpoint retrieves any of a number of appropriate records from the test data management system.
- The Express endpoint uses the view builder to assemble a response from the data retrieved from the test data management system.
- The Express endpoint returns the response built (again: given a record or set of records as input) by the view builder method.

Because the endpoints provide records (extracted from the test data management system) to the view builder methods as arguments, I could easily create unit tests agains the view builder methods that leveraged the DTO interfaces I'd used to define schemas for data stored within the test data management system.

## I Made WebSockets Work

As I outline above, the display of the page depended somewhat on the current state of display variable selection, which was selected within an outer page and which was subscribed to by the inner page (namely the page I was tasked with testing). In order to test effectively, I need to be able to set display variables within test runtime and convey current selection state to Angular.

To do this I saw two options: invoke the outer page UI (to select state) somehow in test runtime or replicate state somehow within test runtime. Sensing it would be simpler and more self-contained (thereby more stable) in the long run, I chose the latter.

To accomplish the latter I implemented a WebSocket endpoint that forwarded state to the Angular page, which subscribed to the WebSocket endpoint instead of the production event service. In essence it worked like this:

- State is updated within a collection in LokiJS (by way of the test data management system).
- In response to state being updated, the LokiJS collection sends a message to a custom `EventEmitter`.
- The `EventEmitter` notifies the WebSocket query the test data management system for state and forward updated state to any active clients (in test runtime there would be only one).

The WebSocket endpoint used a heartbeat that used a very short interval (IIRC something like 40ms) and responded to detected hangups quickly in order to avoid leaks related to sessions abandoned by the client (the Angular page rendered within the browser). With this I could refresh the page and expect that the server would flush the abandoned session in favor of any new session established on page reload.

## I Configured Cucumber Lifecycle Hooks to Manage the Mock Backend

On startup (within a Cucumber `BeforeAll` callback), I started the mock API service. The way I did this was very similar to examples I've provided in previous posts:

<pre><code class="language-typescript">
const appContainer = new ApplicationContainer(containerSettings);

appContainer.attachRouteSets([
  new PersonRoutes().at('/people'),
  new PlaceRoutes().at('/places'),
  new ThingRoutes().at('/things'),
]);

appContainer.start();
</code></pre>
For test data teardown I referred to the instance of database that gets instantiated at global scope any time somebody uses the test data management service: LokiJS provides a method that can be used to list all available collections: the way I designed the DAL, the only way a collection would be attached to LokiJS was if it had been called (with the repository's get `collection()` method) during test runtime.

I used distinct naming patterns to name collections for repositories with data I expected to be volatile between tests and for repositories with data that I expected to persist between tests. So if a collection contained test data it would use `testData`. as a prefix, for something like `testData.calendars`. Framework configuration would use `framework`. as a prefix, for something like `framework.configuration`.

At the end of every Cucumber scenario, then, I would iterate through all collections currently attached to the global instance of LokiJS and remove any collection with name that matched the pattern (as outlined above: `testData.*`)  I used for volatile test data.

## I Configured Angular to Proxy to the Mock Backend

This one is a little less clear because I haven't looked at it in a few years. Angular provides [documentation for engineers to create a proxy](https://angular.io/guide/build#proxying-to-a-backend-server) (in essence using [webpack-dev-server](https://www.npmjs.com/package/webpack-dev-server)) for backend calls made within the app. Within this, I could proxy any HTTP call (whether the path was hard-coded or relative) that matched patterns I set within my configuration to an alternative path (and port) of my choosing.

If I recall correctly, we had something like three build targets we managed for the page I was tasked with testing: two of them used proxy settings, and the last (for production) did not. So for ng test, we used a build target that would make use of proxy settings.

## I Configured The Angular App to Inject Dependencies Conditionally, Depending on Build Target Settings Exposed in Runtime

This one I am also a little fuzzy on how I made it work, but I will do my best here.

A design concept that is fairly central to Angular is **dependency injection**. For anybody not familiar, let's try briefly with an analogy terms of fishing: if a fishing boat needs an outboard motor (and technically any motor will do as long as it has a propellor, a fuel line, and tiller handle with a throttle grip -- and it runs), dependency injection will make sure an instance of an class that satisfies the contract for an outboard motor gets installed onto the fishing boat on the class field that serves as a motor mount point. The boat provides a mount point (the flat-panel stern) for any instance of the class of outboard boat motors to attach, and as long as a motor fitting the requirements (in essence satisfies the contract I outline above regarding the propellor, fuel line, etc) can successfully be implemented and used as a dependency of that boat. In essence, it could be said that any actual motor is a an instance of the type required for an outboard boat motor, and that dependency injection ensures that a satisfying instance (configured prior to runtime) is made available. Could be a 25hp Evinrude; could be a 90hp Mercury, could be an electric trolling motor. Depending on how the injection framework is configured to satisfy the dependency, that's what you'll get.

This oversimplifies a bit, but it's about as good as I can do in a single paragraph designed to lead to my next point.

The functionality that the Angular page depended on to get current variable selection state (where users select a person and/ or a calendar that define how a page should display) was a class that used RxJS to subscribe to an instance of Observable.

When an Angular page is run with target test (vs production), Angular allows for setting environment variables (related to the build target the Angular page is currently running under, like `PRODUCTION` or `TEST`) that can be accessed within the page during page runtime. So based on whether the environment variable reflected that current Angular build target was production or test, we injected either the code that subscribed to the production observable or custom code I'd written to subscribe to an Observable defining the WebSocket connection.

So in essence it's the same boat (the page we'd built), but different motor depending on the context we depended on running the boat within. We told dependency injection which one we wanted where, and dependency injection mounted the motor we needed where- and when we needed it.

## I Tested as Much of My Solution as I Could

Hopefully it rings true here my belief that any time spent on building a solution that cannot be validated has likely been wasted somehow. If you build a solution for production then put it in runtime without testing it, how do you know it works? Likely you will make the claim that it works, and in order for consumers to use the solution, they will need to respond to your claims with some level of confidence. What happens if your solution updates somehow, or if a library your solution depends on (or the runtime environment it will deliver value within) potentially changes: can you assure the same level of confidence without testing?

Would you say that without validation you can assure it credibly? That's sort-of the business of Test Engineering.

Along the same lines, it quickly became clear to me that if I did not test any of the solutions I'd built as pieces to solve the puzzle, things could go downhill quickly. Data in the test data management system could become ambiguous somehow. Changes in dependencies could challenge downstream functionality.

The development I undertook actually became TDD. As I built API endpoints, I found issues associating data between different record types that would have been difficult to uncover without automated tests. I also recall issues in view builder methods that, similarly, would not have been detectable without automated tests.

In general, my testing strategy looked like this:

- I built integration tests against the test data management system, including the DAL. This included tests to confirm functionality when the DAL was expected to throw Error messages.
- I built unit-, integration- and system-level tests against the mock API system.
- I wrote unit tests against the view builder methods used by the mock API.
- I wrote limited system-level tests in TypeScript against the test data management and the mock API system. Both systems were written in JavaScript with custom types.d.to files; I wrote system-level tests in TypeScript to basically validate at a high level that the library worked when consumed within TypeScript.

So at the same time I built systems to support testing, I built testing out in support of those systems. I used it to help ensure that, before we built the puzzle, the pieces all behaved the ways they were expected to.

## Exploring Testing Results

We (the delivery team responsible for the page I was tasked with testing) ended up with a suite of roughly 300 Cucumber scenarios. It was fairly comprehensive, but in my opinion there was room to be more comprehensive. The tests took us about three minutes to run at any given time.

At one point another team demoed a suite of 300 tests they had developed against a login screen, using Cypress. The suite ran against the full production backend populated with a set of generic test data. It took about 30 minutes to run, which was ten times longer than our suite took (per the numbers I ran, the same as saying our suite was 90% faster: take your pick).

If I recall correctly their suite may have failed a couple times due to errors resulting from concurrency issues related to running against the full stack. Any time there was an error, the suite needed to be started over. Our suite did have an intermittent issue (I suspect it was related to the custom EventEmitter I'd written to link data events in a LokiJS collection to transmission to WebSocket clients) that I believe I could have fixed if I hadn't been reassigned.

At one point the team responsible for the UI component library implemented an upstream change to the version of Angular all pages using the component library were expected to upgrade to. Following the update, everybody was expected to upgrade the Angular dependency for their pages (and perform regression testing) at the same time. If I recall correctly, more than a few teams needed to stop the feature development they were working on for at least a sprint, to pivot to manual regression testing.

Our regression tests took roughly twelve minutes: roughly three minutes against each major browser (Chrome, Firefox, Safari, and Edge) we ran against, although we did need to update one part of our setup that Angular broke before we could run it. So twelve minutes give-or-take a minute or two to execute the runs where we discovered this regression.

As a bonus, software engineers on the team I served on (and on another team that started using our solution) asked for instruction to be able to set up instances of the Express mock backend independent of test runtime as a fixture for manual testing of their respective Angular pages. Once they understood how to start Express (using `applicationContiner.start()`) and add data (using the DAL within the test data management system), they were free to test on their own.

## Conclusion

I believe the argument could easily be made here that this solution effectively reinvented the wheel. In response I might suggest that what this solution did was effectively built an N-Tier Web app within test runtime. This put tests on firmer footing and reduced the number of times we might need to reinvent the wheel in testing -- both for the page I was tasked with testing and any page developed within the organization that potentially also used this solution.

This seems like a lot of extra work, but it ended up simplifying the testing problem. Once I had test support systems in place, and I was able to link the parts together, I had something that I could reuse to help another team get started testing with the same system. Once I understood how everything fit together, it was relatively simple.

For me generally speaking the numbers validated my hypothesis: 3 minutes for 300 UI tests (especially at a 90% reduction when compared to running a comparable suite e2e) is great. And the solution overall was reusable.

I wouldn't call this a perfect solution. Again: we encountered rare intermittent failures that I'm very confident were related to a custom `EventEmitter` I'd built and which I'm also confident were easily fixable with the right resources. The first time I build this system (all together), there was no problem using canned static images (IIRC at one point I wanted to use images of playing cards in place of profile pictures for people records). If I had to use this with a system that depended on resources (for example, resources cached from another system) this might present an additional challenge.

Despite this, the solution is relatively versatile and future-proof. Express and http.Server are very stable. When you dig into [the code used to define basic functionality for LokiJS](https://github.com/techfort/LokiJS/blob/master/src/lokijs.js), it's effectively an array of arrays (that also function as EventEmitters). And by using the architecture I've outlined here, concerns related to test data management and data transport are kept clear of any interaction with the browser (and generally independent from one another) beyond HTTP calls the browser makes to request data. As such, it should work with any browser (no matter how old), and it should work with any test runner and UI automation tool.

With what I generally understand about mobile app test automation (in essence: [appium runs in JavaScript](https://www.npmjs.com/package/appium)), it seems like an overall solution like this might be portable to mobile testing, as well.

In a couple different ways this solution also minimized the risk presented by any given test run. When any one test fails, the investment to confirm a fix generally involves an equal investment in the same number of tests running again (to verify the fix); if tests only run for 3 minutes, any failure requires another 3 minutes to confirm a fix (compare that to a 30-minute run). At the same time, tests limited risk by limiting involvement by outside systems in work related to managing tests (especially related to managing test data); the overall solution outlined here reduced the possibility that any one full-size system might produce an issue by using mocks that were robust enough to be configurable (and usable) for testing in many contexts but also designed in such a way that they made themselves open to debugging.

Which as I understand it gets test automation engineers closer to solving the problem they were tasked with initially anyway.