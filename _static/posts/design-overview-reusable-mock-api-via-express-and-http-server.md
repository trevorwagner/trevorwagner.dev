---
title: "Design Overview: Reusable Mock API with Modular Routing Using Express/ http.Server and Optional WebSockets"
publishDate: "2023-08-08T15:38:00-05:00"
coverPhoto: "https://static.trevorwagner.dev/images/anthony-U8Zj6ihgEkc-unsplash/1200x800.jpg"
thumbnail: "https://static.trevorwagner.dev/images/anthony-U8Zj6ihgEkc-unsplash/300x200.jpg"
draft: false

---

At one point I was working on a project that led me to develop the in-memory test data management system that I describe in another post.  At the same time I needed a place to manage test data, I also needed a method of conveyance to get whatever test data I was storing to the Angular app I was testing at the time.  If I was going to build something custom, it made sense to make whatever that ended up becoming reusable.  

In this post I will describe the system I ultimately built to make this work: a modular mock API service built on top of Express and node's built-in `http.Server`.

I've been advised that there are solutions other than the one I outline here that also facilitate transport of test data between a test data management and the application surface.  I'll talk a little about these alternatives, as well in context of the solution.  In general I believe this is a comparatively stable solution that is not browser-dependent, is open to testing, and provides support for use cases outside of testing.

Beyond any implementation I've made of this system for companies I've worked with, I have also implemented this solution on my own time with my own resources.  What I'll be describing in this post is a version of this solution I've written independently.

## Overview/ Understanding the Problem

I was tasked with testing the UI in an Angular that was part of a full-stack solution that involved multiple runtimes and a lot of unwieldy data.  The full stack was a 3-tier solution with layers that looked like this:

- **Presentation Layer:** Angular.
- **Business Layer:** Java, serving two APIs (one RESTful and the other SOAPish).
- **Data Layer:** RDBMS (i.e. SQL).

In order to manage test data and limit non-determinism related to the external systems I needed to make a choice:* accept the full stack as an external dependency for testing, or attempt to work around it.*  Ultimately I chose to work around the full stack, opting instead to write a system that managed test data independently of the business- and data layers.

In addition to managing test data, I also needed some sort of transport layer to handle mocking API endpoints consumed by the Angular app and provide mock business logic between the data management system and Angular.  I was aware that Express gave me a couple tools that I could use to attempt to build a solution that I was confident in.

## Starting and Stopping an Express Server in JavaScript Test Runtime

It is possible to configure and start an Express server instance completely within test runtime.  If it helps, I've actually posted [an example project on GitHub to show what this looks like when it works.](https://github.com/trevorwagner/js-jasmine-run-express)  The example I've written uses Jasmine; I've also done this with mocha, and I presume it should be possible to use this with any general JavaScript test runner (for example Jest).  There really isn't anything fancy here: just run the right code in the right spots, and you have a usable HTTP server during test runtime.  

For anybody who potentially wants to try this, there are three things worth keeping in mind:

- If `http.Server` (which Express effectively runs on top of) is not shut down within the test run (i.e. sometime while Jasmine is running), Jasmine will throw an error.  So if you use this pattern in CI, you will want to stop `http.Server` or else failure to stop will fail any runs that use it.
- It is not possible to stop Express directly, but it is possible to stop `http.Server`.
- It is possible to convert an instance of Express to `http.Server` (using `http.createServer()` like I do here), but once that happens Express endpoint definitions can no longer be added to `http.Server`.  If I understand correctly, `http.createServer()` is in essence a factory method that produces new instances of `http.Server` given an instance of `express.Application`.  My understanding might be incorrect here.

### Express Routers Make Endpoint Definitions Modular

Express provides a class [Router](https://expressjs.com/en/api.html#router) that serves as a mount point for a set of routes.  It is possible to define routes for an instance of `express.Router` and once that router is mounted to express at a specific relative path, all of the routes defined for the Router are also routed relative to the relative path the Router was mounted at (using `app.use()`).  

So if you define your router (and a route for it) like this:

<pre><code class="language-javascript">
const greetingsRouter = express.Router();

router.get(‘sayHello', (req, res) => {
    res.send(‘hello world!');
});
</code></pre>

…then you attach the route to Express, using `app.use()` like this:

<pre><code class="language-javascript">
const app = express();

app.use(‘/whyNot', greetingsRouter);
app.listen(3000, ()=>{console.log(‘Express running on port 3000.')} );
</code></pre>

If you submit a GET request to http://localhost:3000/whyNot/sayHello, the server will return the response body hello world!.

Using `express.Router` in this manner creates two opportunities for test support code:

- Make sets of express routes modular: if I attach a set of routes to an instance of `express.Router`, then I can in essence attach that Router to any instance of Express (at a relative path of my choice).
- Define behaviors for an instance of `http.Server` that, given any set number of instances of `express.Router` (attached with `app.use()`) should configure a reusable mock API and provide methods to start and stop the server.

To make this work I will need a few [wrapper classes](https://en.wikipedia.org/wiki/Adapter_pattern).  More on this in Tech Stack/ Design (see below).

## HTTP- and WebSocket Connections Build on `http.Server`

When I built this originally I needed both HTTP and WebSocket connections to make the mock backend work.  By this point in this post, the use case for the HTTP endpoints was hopefully obvious: I needed to be able to replicate HTTP endpoints consumed by Angular in production.  The WebSocket endpoint I used had a specific purpose: to provide realtime data transmission of display variable selection state data events simulating an EventEmitter used in production UI that the page under test subscribed to via RxJS.

For anybody who didn't follow that, I'll unpack my description a little briefly.  The system under test (the Angular page) was part of a larger system that allowed users to specify which data would populate (on our page) based on input supplied to Web UI controls.  In essence it was like a UI to be able to set URL query parameters that were then passed to the page by way of display variables set within the selection UI.  In production, our page lived within an `<IFRAME>` element that was nested within the larger display variable selection that provided the controls: if a user used the controls to select a resource to display on the page (to specify a person record, for example, that they would like to view), our page (within the `<IFRAME>`) would respond once the EventEmitter it had subscribed to (via RxJS) fired an event with updated variable selection state, and would effectively reload to display data for the new display variable selection state.

The UI to specify display variable selection presents a lot of work to manage in test runtime, especially if the testing system decouples the page under test from the full stack backend.  So I decided to simulate the Web UI (used to specify page display variable selection) in code by storing the current variable selection state in the test data management system, listening to LokiJS collection events for inserts or updates, and forwarding the new state over WebSocket connection (which during test runtime the page subscribed to via RxJS instead of the production UI EventEmitter.

To get back to the main topic, then: I also needed a WebSocket connection.  Hopefully it's clear now why.  WebSockets can be attached to `http.Server` but not Express.  Fortunately I already need to convert Express to `http.Server` in order to be able to shut it down at the end of test runtime (see **Starting and Stopping an Express Server in JavaScript Test Runtime**, above).  

## Tech Stack/ Design

Beyond the built-in http package, [Express](https://www.npmjs.com/package/express) is a critical part of what makes the modularity and portability of routes work.  To make WebSockets work I import [ws](https://www.npmjs.com/package/ws).  

As I note within **Express Routers Make Endpoint Definitions Modular** (above), I needed a few wrapper classes to make this work.  I ended up needing a wrapper around instances of `express.Router` and the routes defined for them (I refer to these as routeSets — see below).  I'd also need a wrapper around `http.Server` that provided storage for settings and utility methods that made it possible to define settings and start and stop the server.

Again: I want users to be able to configure a server with a minimum of highly-readable code.  

### RouteSet Wrapper Class

RouteSet is a base class that establishes a wrapper around `express.Router` stored on instances of the class.  This wrapper class provides a lifecycle hook (setRoutes()) that allows users to define any number of custom subclasses (sometimes I refer to these as "route classes") that they can attach using Express (see AppContainer Wrapper Class, below) as the custom classes are instantiated:

<pre><code class="language-typescript">
appContainer.attachRouteSets([
    new PersonRoutes().at(‘/people'),
    new PlaceRoutes().at(‘/places'),
    new ThingRoutes().at(‘/things'),
]);
</code></pre>

The first time I wrote this library, I only established a wrapper around HTTP routes (not for WebSocket endpoints).  For WebSocket routes (of which at the time I only needed one), I attached it directly to the instance of `http.Server` after it was extracted from express.Application (using `http.createServer()`).  To make the design more modular I eventually established two RouteSet base classes: one routeSet for HTTP routes and one that establishes a similar sort of wrapper around WebSocket ws routes.  Both support using at() right after instantiation as outlined in the above code snippet.

Because WebSocket routes are a little more complex to define behaviors for to maintain contact with active clients, it requires a little more code to make work.  Among other reasons: WebSocket is message-based and JavaScript is event-driven (so we will need to define behaviors in terms of message event callbacks).  What's more, the establishment of WebSocket routes require upgrading an HTTP request (which means more event callbacks).  Furthermore, the server is generally expected to manage open WebSocket client connections and establish heartbeat routines that expect "pong" responses by the client in response to the server's "ping."  All of this needs to be handled somehow in code (more event callbacks here, too).

When I wrote this again later, I wrote two subclasses for RouteSet (one for each transmission type): **HTTPRouteSet** and **WSRouteSet**.

### AppContainer Wrapper Class

AppContainer establishes a wrapper around a specific instance of `http.Server`.  It stores a set of configuration options (basic express configuration), an instance of `http.Server`, an array of attached routeSets, and a boolean field isRunning.

AppContainer provides four methods:

- `attachRouteSets()`: allows for setting instances of `RouteSet` at a relative path.
- `attachRouteSet()`: for anybody who would like to (for whatever reason) attach a single `RouteSet` but would rather not create an array for just one item.
- `start()`: bootstraps converting express to `http.Server`; then, starts `http.Server` and sets `isRunning` to `true`.
- `stop()`: stops `http.Server`, and sets `isRunning` to `false`.

Configuration options (for example, the port `http.Server` should listen on, the service name label used to identify `http.Server` in logs) are set via the constructor.

### TypeScript Types

Because most of the low-level work here is done by JavaScript, I'm not sure there would be value in attempting to write this library in TypeScript.  In general, because this is a test support library, any library that consumed it would likely either need the library to be transpiled or for the library to be in a place that can be imported from.  Without getting into the details, I've written this library in TypeScript.  At first I imported it directly to testing projects (i.e. sets of code that tested against the system under test) that depended on it; this resulted in a number of headaches that led me to explore transpiling.  If I recall correctly, attempting to transpile led to its own set of headaches that led me to re-evaluate whether it was worthwhile to write in TypeScript to begin with.

In general, my experience has been that it reduces overhead (a lot) to build this library in JavaScript and type it with a custom types.d.ts file.  Just obtain the code and use it; no need to transpile or host artifacts.  If you want to run tests, the JavaScript code is ready to test.

## Exploring Alternatives

It was brought to my attention sometime later that there are alternative libraries that allow engineers to mock API calls within the browser directly or intercept outbound API calls and provide responses to them.

I still think this is the right way to go about solving the testing problem when I consider the following:

1. Solutions that mock HTTP calls leverage APIs within the browser somehow that appear to intercept or interact with what would have been an HTTP call made by the browser.  When testing with a browser (especially when testing cross-browser), I have found that it pays to approach testing as though the browser is part of the system under test: the browser is part of the operating environment that that (along with any pages loaded/ rendered therewithin) provide value to consumers.  Along the same lines, I try to avoid (as a matter of practice) anything that can be expected to alter this relationship, however slightly.  If it helps, I realize how superstitious this might sound as an engineer; as a tester, though, it's elementary that deviation from production presents the possibility for regressions in test runtime.
2. Not all browsers support the browser APIs used to make the mock APIs work.  Some software companies (in some cases, under contract) still support older browsers.  That being said, as older browsers approach end of support I expect this argument to grow less valid by the day.  But until they do, they present their own specialized areas of risk that are likely worth testing against.
3. Every HTTPRouteSet or WSRouteSet built with this system is potentially sharable.  So for any endpoint that gets consumed by more than one page/ app, it should (hopefully) not be necessary to produce multiple mocks of the same endpoint.  By sharing endpoints in this manner, I would expect any impacts following a change to a mock endpoint (ideally, reflecting changes in any production endpoints being mocked) to show in test results of pages or apps that depend on the shared mock. 
4. Every RouteSet class is also testable as an HTTP endpoint.
5. The technologies this solution uses are so stable and old-hat that they seem very unlikely to change.  Unless something fundamental changes in Express, `http.Server`, or ws, functionality (and thereby value) provided here is likely safe to put into use long-term and forget about.
6. The solution I've presented here is usable outside of test runtime for manual testing.  So if you potentially have an engineer who would like to test complex data setups (which was the case for me the first time I wrote this library), this library can also be helpful for that.

I also believe there's potentially room to use a solution like this with mobile testing, which may be worth factoring into any decision-making.  If an organization offered both a Web-based solution and a solution (somehow) encapsulated within a mobile app, any automated testing performed within the app in JavaScript (e.g. with Appium), the could expect to enjoy all of the benefits for each testing effort in a unified, reusable mock API.  

As long as I'm taking requests I understand that fastify is also an option to accomplish a lot of what I'm doing off the shelf.  I actually found fastify while looking for a way to provide custom types for this library.  Fastify supports WebSockets with the use of a plugin.  Fastify has also released two major version upgrades since I wrote this library initially (early 2020), each of which required following a guide to upgrade from.  

Conclusion

Let's say somebody wanted to use this (for some reason) within a Jasmine describe() block.  Assuming the routes within PersonRouteSet were already defined, here's the code they'd need to make it work:

<pre><code class="language-typescript">
import { ApplicationContainer } from 'reusable-mock-api-service';
import { PersonRouteSet } from '../../routes/custom-routers/';

describe('my functionality', () => {
    const applicationContainer = new ApplicationContainer({ port: 3000 });

    beforeAll(()=>{
        applicationContainer.attachRouteSets([
            new PersonRouteSet().at('/people');
        ]);

        applicationContainer.start();
    });

    afterAll(()=>{
        applicationContainer.stop();
    });
});
</code></pre>

At this point, any routes defined within PersonRouteSet are available for interaction during test runtime, and the server will close down gracefully within the afterAll() statement.

Meanwhile, the design I provide here is a simple, easy-to-use system based on three packages (Express, `http.Server`, and ws, as I note above, under Exploring Alternatives) are stable enough that I wouldn't anticipate to change any time soon.

With the system I built, any users require (potentially) two general areas of familiarity:

How to set a route (ideally on Router) in Express.

How to configure a WebSocket using ws.  It might also help here also to understand generally how WebSockets work more generally.

To me all of this seems pretty easy.  If it were up to me again, I'd build something like this (again).