---
title: "Three Rings: A Simple Model to Organize Test Planning"
publishDate: "2023-06-25T12:46:00-05:00"
coverPhoto: "https://static.trevorwagner.dev/images/willian-justen-de-vasconcellos-rM9V6BjNaKM-unsplash/1200x800.jpg"
thumbnail: "https://static.trevorwagner.dev/images/willian-justen-de-vasconcellos-rM9V6BjNaKM-unsplash/300x200.jpg"
draft: false

---

[In a previous post I outline how I generally approach test planning](/blog/posts/how-i-write-test-plans-for-new-functionality/): I create an inspection checklist that asks questions that specifically seek to gather information that can be used to address user concerns. Within this, it's important to design the questions that the checklist uses to expect a simple yes/ no response. For example:

- *Q: When the toggle is switched to the `ON` position, is functionality behind the toggle enabled as expected?*

Here, switching the toggle to `ON` either enables functionality behind the toggle or it doesn't.

When you reach beyond simply evaluating functionality, though, it can be easy to get lost in the details. Some workflows exercise specific functional areas but not others. Some workflows exercise multiple functional areas. And when your primary focus in test planning is to cover user concerns (not just functional areas), it can be a challenge to find a workflow that exercises specific functionality. I've actually found that test planners who don't use a model can sometimes get turned around.  

Along the same lines, it can be easy to create waste here, too: without a method of organizing the relationships between different concerns, any concern and any use case is basically just as valuable (and worthy of testing on its own) as any other.

There's a model I use for this; it helps me organize.  I don't use deliberately, but I find I use it. I envision the model as a set of three nested rings. It's not especially original, but it works for me in a couple different ways. The innermost ring provides essential functionality. Outer rings describe use case concerns that rely on inner rings, so if you run a test in an outer ring, you can expect that you might also provide additional coverage on concerns in an inner ring. So basically when you test within a ring, expect that anything within that ring (including rings inside of it) get some coverage.

Regardless of whether you write test plans the way I outlined in the previous post, the model I provide here might be helpful as another avenue to organize testing. It's a great way to start with what you know an reach out as far into the unknown as you can.

## Inner Ring: Essential Functionality

If you sell something you've built, there are a set of attributes and behaviors that make it recognizable within its value proposition as a product. Let's say your product is a door. Most likely, you are going to expect it to be a slab (functionally presenting a barrier between one side and the other) of some sort, you expect it to move (to swing open or closed in some examples, or to slide open or closed in other examples), and to latch and unlatch.

If it doesn't do these things, it's likely not recognizable as a door. So if I were writing a test plan against the door, I'd want to add questions targeting each functional parameter listed above.

If I was testing an API endpoint that accepted POST requests to submit data, I might start with questions like these:

- *Q: If a user submits a POST request to the API endpoint, does it return a response?*
- *Q: If a user submits a POST request to the API endpoint, does it return the expected HTTP response codes?*
 - The request is valid.
 - The request is invalid (there might be more than one variation on an invalid request; list them here).
- *Q: If a user submits a POST request to the API endpoint, does it return the expected response message?*
 - The request is valid.
 - The request is invalid (again: there might be variations on an invalid request).

Here we're just making sure that the API exhibits the essential API behaviors we expect it to. It actually works a lot like a door: it provides a barrier that can open to allow ingress and egress as needed.

When I pose questions about essential functionality, I generally do my best to be as exhaustive as possible, but at the same time I try to be clear about questions that seem to describe use cases more than they do general functionality. Use cases come next, starting with the most common.

## Middle Ring: Concerns Related to Common Use Cases

Within the product that you build, there is a set of use cases that almost everybody can be expected to use. Your product (or functionality under development) will likely make it possible to do at least a couple key things, and what it takes to get those things done are effectively workflows. In order to get the things done that require the workflow, the associated workflow will likely incorporate essential functionality in service of users' most common concerns. These are generally going to be your expected use cases or most-common use cases.

Imagine how most people test doors by swinging- or sliding them briefly. The test incorporates exercising essential functionality (the slab swings or slides as expected) with a brief user acceptance test of the suitability of the door to *swing on the hinge or track as though it were being opened or closed*.

Where I come from it's generally customary in case of success in executing the sort of test outlined here to declare "yep: it's a door."

If I unlatch the door latch and push (or pull, depending on how the door is expected to swing or slide), does it open completely as expected? If I pull the door shut, does the latch engage as expected? These are use cases that can be expected to be valuable to most users, and because nearly everybody can be expected to use them, the system under test should be expected to support them.

Let's look at the POST endpoint, again too. Does the endpoint accept a request with valid payload? Depending on whether saving data is a concern with your endpoint (I generally try not to test ETL via e2e testing against API endpoints): if a user makes a request to a different endpoint for data that was just POSTed, does the data submitted via POST persisted in the system? Does the endpoint accept a request from an authenticated user? How about from an unauthenticated user, or a user with sufficient/ insufficient CRUD privileges?

When listing concerns, any overlap between use cases and functionality is fine, even if in most other cases it might seem silly: when planning testing, one of the most important things is to limit opportunities to potentially miss something. What's more actually end up with additional opportunities to coverage of your essential functionality -- likely from a perspective that was different from the one you tested essential functionality with initially. What's more: as a test planner it's within my purview to remove a question from the test plan, and when executing tests it is within my purview to mark a test with a status of `N/A`.

I believe this is different, by-the-way, from happy-path testing. Happy-path essentially combines essential functionality and common use cases, in attempt to cover both at once. Does the door open? Does it close? If all you were interested in here was happy-path testing, then clearly you have a door.

## Outer Ring: Concerns Related to Less-Common Use Cases

Beyond common use cases there are use cases that likely not used by many users if at all. These use cases present concerns that may or may not be immediately evident to most users. They may be stumbled upon by accident. Nevertheless it's likely important to at least consider them (if not also test them) when planning testing.

Once I've listed concerns related to essential functionality and common use cases, I reach a little further to try to find valid concerns related to these less-common use cases.

They frequently incorporate concerns related to common use cases and essential functionality. But with this in mind: the set of uncommon use casese the system under test can be expected to support is likely a function of the composition of the system itself.

If you slam a door, for example, will it remain on its hinges? This is likely not a use case not many users can expect to encounter frequently, if at all. Sometimes doors slam unexpectedly, for example in response to a cross-ventilation within a building. If the door is made of tempered glass (again: an implementation detail), this could present issues.

How resilient is the door to an attempted break-in? How well does the door hold up in a house fire? What is the R value of the door? At one point I lived in a house with a decorative door (with several lites of single-pane glass) separating the porch from the living room. By the way: this was in Minnesota, so I found out around November that the door had low R value.

If you submit a payload with malformed XML or JSON to a POST endpoint, will the endpoint behave as expected? How about if you attempt to make a request for a user that does not exist? What you've attempted to submit POST with a valid user, but session tokens have expired (is this an endpoint concern, or is it a concern better suited to testing session management functionality that the endpoint incorporates)? What if the endpoint is part of a system that uses CRUD permissions: are the permissions expected to be cumulative (i.e. granted Write permissions imply that Read has also been granted)? All of this will likely depend on the design decisions (conscious or not) you arrived at to define how your endpoint would be implemented.

## Conclusion

When writing test plans, it's not just a single perspective that we seek to test in support of; it's actually many. And while it helps to validate functionality and anticipate concerns, my experience has been that, without some sort of method to organize how we approach describing the concerns we mean to support in testing, we can easily get turned around and create waste. Whether or not I find I'm using it deliberately, the three ring model I use helps me organize both where concerns relate to each other and how the concerns will ultimately get tested.

I start with essential functionality, then move outward. If I can confirm that essential functionality works as expected, I can also start confirming that use cases that depend on that functionality are supported (and that, in turn: concerns related to those use cases are supported).  And as I continue to test, the overlaps this model helps make me aware of keep me in the driver's seat either to get additional coverage of an inner ring or to decide not to continue testing.

This goes beyond testing for functional- and nonfunctional requirements, because the model provided here aligns testing inquiries to stakeholder concerns and generally ranks those concerns in terms of how central a concern is to what the team essentially intends to ship.