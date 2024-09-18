---
title: "Design Overview: In-Memory Generic Repository for Storing Test Data in JavaScript using LokiJS"
publishDate: "2023-08-01T17:49:00-05:00"
coverPhoto: "karen-tsoi-CXMzH6dMobQ-unsplash"
draft: false

---

At a couple different points in previous lives I've found myself in a position where it made sense to build an in-memory data management system in JavaScript (also typed for TypeScript). In this post I'll talk briefly about why I designed the system the way I did and what I ended up building. In essence, it uses a [generic repository pattern](https://khalilstemmler.com/articles/typescript-domain-driven-design/repository-dto-mapper/) (built on [LokiJS](https://www.npmjs.com/package/lokijs)) that makes it possible not just to store and recall test data but also to validate it.

Even if your aim is to store and supply mock responses of API calls to a UI front end, it might be a good idea to invest in test data management. Managing test data centrally like this allows the management system to serve as a single source of truth for system state (whether that be in the system under test or even the framework itself) while at the same time providing a predictable set of methods to be able to set and recall full- or partial records with minimal code. This can also help make test cleanup a breeze and provide a reusable system that can also be tested on its own (thereby increasing confidence in testing systems that depend on it).

The same way the generic repository pattern is not new on its own, it's also not new to JavaScript/ TypeScript. The same way: when I originally implemented this project, it wasn't my first time working with in-memory databases. In essence what I built here is based on both, plus data validation and quality-of-life functionality that I believe (and my experience with this system as a tester tells me) is helpful to have when implementing data management for tests.

Beyond any implementation I've made of this system for companies I've worked with, I have also implemented this solution on my own time with my own resources. What I'll be describing in this post is a version of this solution I've written independently.

## Overview/ Understanding the Problem

The main problem I wanted to solve was *how to find a place for CucumberJS steps to effectively store/ manage data while running tests*. As I ran Cucumber steps, I would create data that would need to be stored somewhere in order to be able to persist state (even if just in runtime), and I wanted a system that would do this for me.

In an even-earlier previous life I worked with a testing system designed (at a high level) by an architect who suggested using transactional MySQL queries for ETL testing as opposed to a full database. With this design it ended up just taking a couple minutes to run thousands of tests.

I also understood that I wanted a reusable test mock of data transport for the system under test. This seems like a helpful topic to cover in more detail in a later post. In essence, though, the system under test was a 3-Tier Web app that looked like this:

- **Presentation Layer:** Angular.
- **Business Layer:** Java, serving two APIs (one RESTful and the other SOAPish).
- **Data Layer:** RDBMS (i.e. SQL).

What I wanted to cover specifically were behaviors in the Angular UI, defined by way of a custom layout framework built on top of [Kendo](https://www.telerik.com/kendo-angular-ui/components/layout/). In order to cover the UI, I needed to make a choice: *accept the full stack as an external dependency for testing, or attempt to work around it.*

If I accepted the full stack as a dependency, I'd be dealing with either one- or two external systems (each with their own runtime, own infrastructure, etc), any testing decisions I made would be coupled to its design, it's openness to interaction (i.e. any APIs it presents for interaction), and any interactions generally present between layers of the full stack. If there was a performance bottleneck between the Business Layer, for example, and the Data Layer, that would ultimately count against the performance of the Presentation Layer: it might make tests run longer than it seems like they might need to, or it might result in unexpected test failures. Also, where a Java backend (generally requiring JRE/ JDK, possible app container, Gradle/ Maven, dependencies, paths, etc.) and RDBMS generally require their own system- and application-level configurations, any one test against the front end might also require configuring the system or provisioning a new system (for example, via Docker or Kubernetes) to make the full stack available for testing against a specific deployment.

This seems to present a lot of overhead if what I want most is to be able to test behaviors in the Angular UI. And as time went on, I sensed that this overhead would more than outweigh the effort to develop a well-written mock backend.

If I attempted to work around the full stack, my understanding was that I should have greater control of test data, greater access to logs if something went wrong, and that cleanup (see below) would likely be easier. I could write code within any mock code I wrote to fail fast in case of an issue. I also understood that my resource footprint to test would likely be much smaller, and that I could likely expect smaller test runtime (i.e. run more tests in less time).

I made the choice to attempt to work around coupling testing to the full stack by writing a test mock that replicated the backend. There were two parts to this:

- Test Data Management.
- Mock API. This seems like a good topic for a future post.

Beyond simply making test data management easier (and making a system that was generally reusable), there were a couple of things I understood I'd want if either I used this system or somebody else used it. I describe those briefly below.

In general, I had a couple other assumptions I worked under as I designed this system:

- I believe it's important that tests be easy to clean up.
- Testing code responsible for testing minimizes risk to test system functionality and anything that depends on It.
- Making test support code easily accessible is just as important as with test- and step Methods.
- Proactive test data hygiene generally pays itself off.

## Design: Tech Stack and Document-Matching Paradigm

To manage data I use [LokiJS](https://www.npmjs.com/package/lokijs), which is a library that was (essentially, as I understand it) written to replicate the Mongo API in for local data storage in JavaScript. Data is stored in document format, within collections that provide their own API to be able to create, manage, find, and delete records at a low level. If needed, LokiJS can save to file; by default, though, it keeps everything in memory.

On its own, LokiJS provides a `find()` method that makes it possible to return any documents matching a query. A document returned by LokiJS contains metadata used by LokiJS to track and manage the document, which may- or may not be relevant to test data. This idea of locating records by matching is fairly central to how the data management system I developed works. For example, for a data set with multiple records, the `retrieve()` verb intends to return one (and only one) matching record, and will throw an error (which is logged by the test runner) if it encounters any fewer or any more than one match. At the same time, `retrieveAll()` returns an array of any matches, including an empty array if zero matches are found.

For any methods defining data management or data introspection, the `find()` method in LokiJS essentially serves as the backbone to return any matching documents; the method calling `find()` retrieves and evaluates the results of (including how many matching documents are returned in response to) a search by a consumer.

<pre><code class="language-javascript">
collection
   .chain()
   .find({ field: 'value' })   // <- Query parameters for a document we would like to match.
   .data({ removeMeta: true }) // <- LokiJS option to remove metadata from documents in ResultSet,
                               // which essentially is an array of documents matching the query.
</code></pre>
LokiJS is generally the only library dependency for this project. In one iteration of this project I believe I also recall using [lodash](https://www.npmjs.com/package/lodash) to deep-clone JSON.

## Datastore and Repositories

The data itself is stored within an instance of LokiJS that serves as a global constant. I accomplish this by exporting a new LokiJS database:

<pre><code class="language-javascript">
var database = new loki('database.json');

module.exports = database;
</code></pre>

Within this, the DAL serves as a layer that defines logic to interact with the database. So rather than interact directly with a LokiJS collection, the DAL interacts with the collection at a low level and presents high-level APIs (namely a CRUD API) that facilitates interaction with the data at a high level. Every repository carries its own LokiJS collection as a field that uses `get collection()` as what's effectively a factory method (it retrieves the existing collection from database if it exists; otherwise it creates a new one using methods and fields stored on the repository class).

In naming my repository base classes, I wanted to do something like what Apple does with CoreData: within CoreData, data is assumed to be a first-class entity on its own in runtime and can be persisted whenever needed. I'm not planning on persisting data anywhere other than in runtime, but at the same time I thought that a similar sort of domain-oriented approach to data management might be helpful to make use of what is essentially a custom system easy to access.

I broke the data we'd be managing with this system into two categories: relational- and non-relational data. The two would effectively share a CRUD API, but depending on which type best described (see subheadings below) the data to be managed, the API would function slightly differently (see Repository CRUD API, below).

To external consumers, the library presents a base type for each repository type (one base type for relational data, one base type for non-relational/ tree data) that each implements its own custom CRUD API. Each base repository type (relational/ non-relational) inherits from a common parent repository type that defines behaviors to retrieve a collection (create a new collection if none exists; otherwise return the existing collection), remove all data from the current collection, and so-on. Each individual base repository class implements its own APIs.

### RecordSet

In context of this system, RecordSet essentially provides a list of JSON documents stored within any LokiJS collection. The documents can be shallow, (like a tuple in an SQL table), or they can be deep (like a data tree). One thing that might be worth noting with this is that, due to the nature of its design LokiJS experiences difficulties finding matches for queries against full data trees. So if the document you intend to match is a tree that is five layers deep, and your search query is the same tree (five layers deep), LokiJS may return the error message `fun is not a function`.

With this in mind I generally try to keep documents and schemas for any relational data as shallow as possible, use auxiliary data tables to describe additional values, and view builders to eventually create more complex trees if I needed one for an API response.

### DataSet

DataSet provides what is effectively data tree that in the form of a single JSON dictionary. Within LokiJS by managing a single document in a collection: there is no functionality to find or validate only any particular instance of a document because there is only one document. So when the `retrieve()` is invoked, it returns the whole document.

## Repository CRUD API

To access and manage data I provide a simple CRUD API that implements CRUD verbs (see subheadings below) that facilitate data management. Depending on the repository type, a slightly-different set of CRUD verbs is available.

Any method that creates or modifies data (`create()`, `update()`, `updateFields()`) should return a copy of the data as it now displays in the database (regardless of repository type). This way, consumers can define or reassign a variable as `repository.create(record)` or `repository.update(record)` without needing to do the work to query the data again.

### create

- For RecordSet, create a new document matching the data passed as an argument.

### retrieve

- For RecordSet, return one document (any more- or fewer than one throw an error) matching the provide query.
- For DataSet, returns the entire tree.

### retrieveAll

- For RecordSet, returns an array containing any documents matching the provided search query.

### update

- For RecordSet, overwrite a single instance (any more- or fewer than one throw an error) with the data provided
- For DataSet, overwrite the full data tree with

### updateFields

- For RecordSet, merge existing data of a single matching document (any more- or fewer than one throw an error) with the data provided via argument.
- For DataSet, merge data in the current tree with data provided via argument.

### delete

- For RecordSet, find a single matching document (any more- or fewer than one throw an error).

### deleteAll

- `deleteAll()` is a method that removes the current LokiJS collection from database. The next time a consumer runs anything that interacts with the collection, `get collection()` will spin up (and configure) a new instance.

## Repository Data Introspection Methods

Whenever I've written this system I've used what are effectively three different methods I call "data introspection" methods. These methods allow a consumer to query the database for information on the number of matching documents in terms of the number of matches the query expects.

### containsAny

- returns true if the query matches one or more records; otherwise returns false.

### containsOnlyOne

- returns true if the query returns one (and only one) match; otherwise returns false.

### containsNone

- returns true if the query returns zero matches; otherwise returns false.

### isEmpty

- returns true if no records (or no tree/ an empty tree) is stored in the repository's collection; otherwise returns false.

## Repository Data Checking

If the primary responsibility of this system is to manage test data and central concept to data management is data matching (especially based on partial records) then it seems like that system should also concern itself with avoiding data ambiguity. Here are two cases where ambiguity might occur:

- If a consumer is able to create data with parameters that overlap parameters for a document that already exists in the database (user creates document A then creates document B which matches document A 100% even if document A does not match document B 100%), then the new document the consumer is trying to create cannot be distinguished from the existing document. This operation should throw an error advising the consumer of the ambiguity.
- Let's say a consumer attempts to read (or update, or delete, each of which requires matching) a single document from a RecordSet/ relational data repository but the query provided for the method accessing the data returns more than one match from the collection. At this point it is ambiguous which document within the collection the user means to access. This operation should throw an error advising the consumer of the ambiguity.

Because (at least in my experience) most data sets for test data tend to be very limited, it seems reasonable to expect that the tester understand which data has been entered to the system under test.

Test runtime is a little different from production runtime in that throwing an exception (or `Error` in JavaScript) in test runtime is generally very helpful. Within the overwhelming majority of test runners, throwing an exception within a test method will fail the test. Throwing an exception within a lifecycle method generally causes test runners to report the error as an issue within the containing lifecycle method.

Where the system validates test data, it's just as important that the error messages returned with error messages are easily readable as that the error messages fire at the right time. If somebody needs to dig into the code defining a system in order to understand why an error message was thrown, I take that as an issue with the system. So if an error message can tell me `for the query JSON.stringify( ${query} ) expected to find one result but found ${Object.keys(results).length}: JSON.stringify( ${results} )`. Along with the accompanying stack trace, using exceptions in this manner helps not only to find where the accident happens but also get an idea of what happened to cause it.

## LokiJS Collection Data Events

LokiJS collections are essentially EventEmitters, which means that event listeners can be attached that execute associated callback code any time an event of a specific type has been detected. In the configuration for repositories of each type, I expose lifecycle hooks that allow for attaching these event listeners to the LokiJS collection stored on the repository class.

At one point I was managing combined first/ last name in one table with this: if within a record data was provided for the fields firstName and lastName, I set a callback method to populate data to the fullName field (a separate field) automatically. The option to specify a unique index (see **Options**, below) relies on this functionality to allow consumers to specify a field for which a unique index value should be set any time a record is created within the collection.

At one point I actually had data events hooked up to a WebSocket connection (via an additional custom EventEmitter), so that any sort of data change in a DataSet/ non-relational data repository sent updated state over the WebSocket connection to a listener within the Angular app (subscribed via RxJS).

## Repository Options

As I've used this solution, I've found that one size of data management does not fit all. For example, some data (especially relational data) requires allowing duplicate/ ambiguous data. Also, this solution (as I generally write it) does not manage unique index values for records (for RecordSet data) by default (for example, the way `CREATE INDEX` does in SQL). In some cases this reduces overhead, but sometimes this simplicity comes at the cost of constraining usability. Whenever I build this system, I bake extensibility in.

For one, the system provides a set of options baked in that can be passed via constructor argument to the parent class. In the example provided within Conclusion (below), the consumer sets a value for createIndex, which tells the parent class to set an event listener on the collection that provides a callback to update the value for that field (in the example `personID`) automatically to a unique value (typically I key off of the value stored within the field `$loki`).

As an additional option, the system provides a couple different lifecycle hooks: one that takes place after the parent constructor has run and another immediately after the LokiJS collection managed by the repository is instantiated. So for any consumer who would like to define a custom option, it the design should support adding that option -- either upstream or by way of a subclass.

## TypeScript Types

All of the above I typically write as untyped JavaScript. There are two reasons for this. First, importing LokiJS to a TypeScript library (unless `tsconfig.json` for the project it is imported to allows implicit any) requires management of LokiJS types for what is effectively low-level work that can easily managed and tested in/ via JavaScript. Next, my experience has been that it is a challenge to export this library (written as TypeScript) to be used elsewhere. Finally, any library written in TypeScript generally needs to be transpired; this generally takes time and resources on its own for work that is being done at a very low level.

When the project is written as JavaScript, I can use it in another JavaScript project if I'd like, and I can use it without needing to transpire it. With typed JavaScript, I just need to push code to remote and confirm that tests pass as expected.

In essence, then, the last step is to get the project ready for use within TypeScript. Create a custom `types.d.ts` file, and add a reference to the file within `package.json`.

I do write system-level tests for this library in TypeScript that (among other things) replicate some of the same tests that I run at a lower level in JavaScript.

## Conclusion

When everything is said and done, engineers writing tests can access this system by importing it. To define a new repository, an engineer only needs to write a few short lines of code:

<pre><code class="language-typescript">
Import { RecordSet } from 'test-data-management-system';

// n.b.: `iPerson` is a schema interface/ DTO created to define fields and
// associated data types for a person record.

Class PeopleRecordSet extends RecordSet<iPerson> {
   constructor() {
      Super('people-data', { create-index: 'personID' });
   }
}
</code></pre>

With this, the engineer can take advantage of full CRUD API, data checking, data events and so-on by instantiating the repository where needed in test code:

<pre><code class="language-typescript">
const peopleRecords = new PeopleRecordSet();

const newPerson = peopleRecords.create({ firstName: 'new', lastName: 'person' });
</code></pre>

One line of code to instantiate the repository. Another to create a dictionary that matches a record stored within the repository.

This gets us all of the above, including:

- A single source of truth for test data state.
- Simplified test data cleanup.
- Common CRUD API for repositories.
- Test data validation (with usable error messages).
- Repository data introspection.
- Test data events.
- Custom repository options.
- TypeScript types.