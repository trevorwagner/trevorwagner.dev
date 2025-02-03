---

title: "How Working QC in a Print Shop Helped Me Understand What I Was Looking At in Software QA"
publishDate: "2023-06-16T17:01:00-05:00"
coverPhoto: "christina-rumpf-XWDMmk-yW7Q-unsplash"
draft: false

---

My first full-time job out of college was working for a promotional products distributor that imprints corporate logos on sports equipment. So if you got a golf ball, a baseball, a fishing lure, or a hockey puck with a company logo on it as a promotional item, there's a chance the company I worked for at the time produced it. Emphasis on chance: as I understand it, it's a competitive market, and the companies that produce sports equipment participate in it.

Eventually I started working as a Quality Control Specialist: I manned a desk at the end of the production line and put a set of eyes on every order produced in-house before it was shipped. During the company's busy months (April to October), the factory processed a lot of orders in-house: I'm guessing somewhere between 50 and 100 a day, of various sizes. At one point I remember hearing more than 130; I'm not sure if it's correct, but I've used it a lot in conversation.

In QC, there were effectively two areas of focus in the evaluations I performed:

- That the factory had produced the product requested by the customer, and that the shipping instructions provided on the factory shop floor paperwork reflected information provided on the customer's purchase order.
- That, beyond delivering the product successfully, there was nothing related to either the product or the shipment that might disappoint the customer. For example, confirm that the provided shipping method will meet any in-hands date specified on the PO. That the product was packed in a way that it would likely survive shipping (especially if part of the product involved golf ball cartons or retail packaging for fishing lures).

There was a lot that went into actually evaluating a completed order, and for this post I won't get into all of the details. To those in the know, these areas of focus actually also align with terminology we use in Software QA: the first bullet point describes **functional requirements**, and the second describes **non-functional requirements**.

There are subtle ways, though, that my experience was slightly different, and that's what I'd like to talk about here. Working in a print shop helped me find a sense of the "Why" (BTW I am a big fan of [the "Why"](https://www.youtube.com/watch?v=u4ZoJKF_VuA&t=154s) -- especially in Software QA) that's always seemed at least slightly different from what a lot of other people work from. In particular, what I eventually realized I was evaluating in Software QA was work product, that the work product was expected to reflect customer expectations, and that the level of evaluation needed in order to assure the expected level of quality went beyond just looking for surface-level issues. My experiences working in a print shop grounded me here, and the sorts of things I evaluated (and evaluated for) in Software QA seemed much the same to me as what I remembered from working QC in the print shop.

In case it was potentially helpful, I'd like to share my experiences here.

## Of Course Software Is a Product, Too.

As I continued down my path in Software Quality Assurance and Test Engineering, something I realized is that software is effectively a product, the same way promotional products are.

When I read the last sentence out loud, it sounds a little unnecessarily esoteric. But really, I think it's a statement that seems to escape a lot of software development organizations: the same way hard goods are judged on their ability to deliver value that meets customer expectations, software is judged on its ability to deliver the same kind of value. After all of the advertising exposure and talented sales people, what you really have to reach both current- and potential customers is the value provided by the functionality you deliver.

There are a lot of facets to that value and the environments it gets delivered within, just like dimples on a golf ball.

I think the reason it took me a while to make this connection had to do with the amount of pressure (both explicit and implicit) that conventionally gets put on SQA Engineers and Test Engineers to reduce delivery bottlenecks at the same time they're pressured to increase coverage.

At one point I remember talking with a salesperson at one company I worked at who told me "The stuff your team writes is so easy to sell."

## It Pays to Approach Evaluation Like a Customer.

For me at the QC desk, I understood my job to identify (as much as I could) any opportunities missed thus-far to meet the expectations of the customer (or, if applicable: the customer's customer). As I understood it: if the customer's experience did not meet customer expectations, why pay for the product in the first place?

What if the imprint used a color that was reasonably close but did not match the color provided within the official color-matching book? What if the customer had ordered high-number golf balls but actually 1-4 had been imprinted on? I needed to scratch all of the pad imprints lightly with my fingernail to make sure the ink had cured properly. What if the order requested shipping Ground to Puerto Rico? What if the customer's hand-written PO called for screen printing on the blue panels of an umbrella instead of the white panels (which tend to be what gets printed on conventionally)? These were all things that could potentially have been caught earlier on -- part of the job of QC was to make sure that any potential issues had been caught already.

After the print shop, my next job in QA was at a desktop publisher where I also provided end-user support for a blogging program I provided QA/ QC on. I still remember one user's feedback that for one program I should test in landscape orientation (on an iPhone) as well as portrait. I had missed an issue where (if I recall correctly) the app basically became unusable in landscape mode. It made sense later on, but the first time I tested it didn't: my general reductive understanding as a software engineer was that, because orientation was effectively a view mode, it didn't seem like it should affect whatever functionality beneath it was making the app unusable.

Once I approached testing as evaluation to confirm the system delivers value to meet user concerns, I started catching more potential issues prior to shipment.

## Quality Assurance Takes More Leadership than Just Delegating Evaluation of the Completed Work Product.

At the promotional product distributor, QC was tasked with evaluating completed production orders. The job of the QC Specialist was to look for things (in either of the two areas of focus listed above) and know where and how to look to find them. Theirs were the last sets of eyes and hands before the packaging was sealed and the shipment was shipped.

In back of house, what served to assure quality (when I worked there) was management (or coordination) of production: a manager took responsibility for production by administrating and actively engaging with it. If it wasn't for the work done throughout production to make sure the right people were doing the right things, it stands to reason that the QC specialist would likely have had more work to do (i.e. more orders with issues to disposition). Among other things, this had an effect of freeing QC up to be able to focus on each order (again: by minimizing the number of issues QC was expected to catch later-on).

I've found that all of this transfers nicely to software development. At the first company I provided full-time Software QA for, I was able to anticipate the sorts of questions I would likely ask to clarify design decisions during testing and ask them during planning. Eventually at that company I became more integral to how we planned on those teams -- at first the work we did, and later which functionality we would implement (and how). In essence I was helping to coordinate production, as well as check work output prior to shipment.

Eventually, at another company, I would start writing test plans that helped quiz software engineers on their designs before they ever wrote a line of code. Sometimes they would need to rework designs because the things I'd outlined within a test plan that I planned on testing. Sometimes we would need to rework requirements because we had all operated under assumptions that were not workable. Although we sometimes missed things in refinement, the fact that we caught these issues before we had changes that we were ready to ship ended up saving the organization time and money, and it gave us confidence that we were designing functionality that likely worked better for customers than our first pass likely would have.

## One Set of Eyes Is Not Enough.

By the time a completed order was placed at the QC desk, it had already passed before several sets of eyes and through several different sets of hands. Every set of eyes and hands involved had a role to play in making sure that the product met both the customer's expectations, as well as our own.

If an issue reached the QC desk, it means that issue also passed through the hands and eyes of everybody who had handled the order so far. Everybody was a lot of people, but for a high-volume shop (especially during its busy season), issues might slip through occasionally.

At the same time, the same way anybody could miss the issue earlier, the QC Specialist could also miss the issue. And sometimes the QC Specialist did miss issues: if I did, I could trust I'd hear about it later. By my recollection, the ratio of misses to at-bats (or even to hits) at the QC desk was pretty low. But I would attribute this as much to the general lack of issues reaching the QC desk as much as I would to anything QC on its own was doing. Everybody had an opportunity to check and re-check (and raise an issue) if necessary. Although operations at the print shop had been optimized as much as possible, it was also an important part of doing business that every link in the chain shared the job of supporting product quality.

On software development teams, something I've found is that QA actually has an opportunity to raise questions (if not also concerns) with Software Engineers and Product Owners on what they are building, and that sometimes raising these questions and concerns pays off. Alternatively, sometimes "well it's just a REST API" turns into several weeks of reworks because an opportunity to confirm something like the format of responses or backwards compatibility was missed, if not discouraged. If the team can be given (or gives itself) the freedom to ask these questions proactively (and it can make itself open to asking these questions) proactively, my experience has been that it stands a better chance of supporting quality in a similar way.

## The Ecosystem Is Just as Important to the Solution as the Product Itself.

When I evaluated completed production orders, part of what I was tasked with was thinking ahead about concerns related to shipping. For one, I was responsible for making sure that any shipping method the order was actually shipped with would meet an in-hands if one had been specified by the customer (for this I had UPS and FedEx ). This was especially important if the customer had specified an expedited shipping method: they were paying more for shipment, so if the product wasn't going to make it there on time (or if they had paid a rush charge for faster turnaround time in the factory), it seemed reasonable that they should know prior to shipment if the selected shipping method might not meet the specified in-hands date.

None of this has anything to do with the product that was being evaluated, but as I understand it, it was important to customer experience (and with it, customer satisfaction).

In software development, I've often found that the concerns related to quality seem to start and end with the functionality or system under development. Test Engineering departments conventionally pour all of their resources into planning and maintaining tests against the product.

In Software QA, two of my favorite things to ask about in planning is how a design decision might affect Support and how the system might otherwise encourage debugging. Anybody can build a thing, but we are almost certainly going to need to debug it at some point. Support will likely have to lead customers through how to untangle a workflow on its own or a customer's intent from the implementation.