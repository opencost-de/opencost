<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
<!-- markdownlint-disable MD003 MD033 MD034 -->

The openCost metadata schemas
=============================

The aim of the project openCost is to create a technical infrastructure that
makes publication costs freely accessible and interchangeable via standardized
interfaces and formats.

In a first step, the openCost team is developing a metadata schema in
collaboration with (inter)national experts for which it proposes an
xml-representation that is particularly suitable for exchange via OAI-PMH. The
metadata schema attempts to consider all costs related to publication („total
cost of publishing”), including Open Access and non-Open-Access costs as well as
costs for processing fees (e.g. costs for bank transfer, credit cards etc.).
The intended goal is to provide an overview over all payments to publishing
houses made by an institution (the so-called _information budget_). In addition,
the standardized, machine-readable format enables easy exchange of cost data
worldwide.

This repository tracks the evolution of the relevant schemas including their
[documentation](https://github.com/opencost-de/opencost/tree/main/doc).

Since we want to involve the community in our work as early as possible, we have
decided to publish our project results successively and to make a first draft
available as a request for comment now.

In a first step we developed a [metadata schema for _fee-based, individual articles_](https://github.com/opencost-de/opencost/tree/main/doc#data-schema-for-individual-articles-opencostpublication) (`opencost:publication`).
A common use case would be articles in Gold Open Access journals funded by APCs.
However, this schema already includes the coverage of cost items beyond Open
Access fees. In a second step, we developed a [schema that includes costs from
so-called transformative agreements](https://github.com/opencost-de/opencost/tree/main/doc#data-schema-for-contractstransformative-agreements-opencostcontract) (`opencost:contract`). Special payment modalities, such as DEAL,
were abstracted and mapped accordingly. Both schemes are applicable for open access,
transformative agreements and subscription fees.

The openCost team invites you to participate in the development of the metadata
schema and is looking forward to a constructive discussion! Please feel free to
open [issues](https://github.com/opencost-de/opencost/issues) in this repository so we can address your suggestions easily and
nothing gets lost. Alternatively, comment on our [web site](https://www.opencost.de/) or send us feedback by
[email](mailto:opencost.info@mailman.uni-regensburg.de). We will then convert them to issues for you.

More information about our project you will find on our website [www.opencost.de](https://www.opencost.de).

<!-- vim: spell spelllang=en_gb bomb
-->

