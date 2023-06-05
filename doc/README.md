# openCost Metadata Schemes for Publication Cost Exchange

Scholarly publications are very well described by standardized metadata.
Existing frameworks focus on 

- bibliographic description
- legal aspects including access rights
- technical metadata like size of files etc.

However, up to now - at least to our knowledge - there exists no metadata
schema to describe _financial_ aspects of publications. On the other hand
_transparency_ for costs is imperative for the transformation of scholarly
publishing to Open Access (OA) if one wants to avoid ever increasing costs.

In collaboration with several stakeholders and close interaction with the
community our goal is to develop schemas for payment data to fill this gap.
During our [first workshop](https://indico.desy.de/event/35620) we already
identified the need to model 

- payments for single articles (e.g. classical APCs, but also colour or page
  charges)
- transformative agreements (e.g. contracts like [DEAL](https://www.projekt-deal.de/about-deal/) in Germany)
- memberships (e.g. contracts like [SCOAP³](https://scoap3.org/))

but also keep the easy adoption for subscription costs in mind. We also
positively identified the need to consider all costs related to publication (_Total cost of
Publishing_) including both OA (e.g. APC), non-OA (e.g. page or colour charges)
costs as well as costs for other processing fees (like costs for bank transfer,
credit cards etc.). In our approach we try to get an overview over all payments
of an institution related to scientific publishing (so called _information
budget_). With the goal of a standardized, machine readable format in mind we
try to achieve a broader understanding of payments, enable easy exchange of data
both inside the institutions as well as in larger contexts on national or global
levels.

For data exchange openCost proposes the well adopted
[OAI-PMH protocol](https://www.openarchives.org/pmh/) which leads us to
initially propose an XML serialization of our format.

Here we  introduce our meta data schemes for further discussion. You can compare
the schema to your payment, ask about any doubts, and are invited to upload
further examples.

Let's start the discussion!

# Payments for individual articles

The overall tree structure looks like this:
```
publication
    |
    |--- primary_identifier
    |        |
    |        |--- doi  _OR_  bibliographic_information
    |
    |--- secondary_identifiers
    |        |
    |        |--- id type=doi
    |        |--- id type=local
    |        |--- id type=oai
    |
    |--- institution
    |       |
    |       |--- institution_id type=ror
    |       |--- institution_name type=short
    |
    |--- type
    |--- external_costsplitting
    |--- cost_data
    |     |
    |     |--- invoice
    |     |      |
    |     |      |--- amount_invoice
    |     |      |--- dates
    |     |      |      |
    |     |      |      |--- date_paid
    |     |      |      |--- date_invoice
    |     |      |--- creditor
    |     |      |--- invoice_number
    |     |      |--- amounts_paid
    |     |             |
    |     |             |--- amount_paid
    |     |             |--- amount_paid
    |     |
    |     |--- invoice
    |
    |--- (part of contract)
```

In XML we use the namespace `opencost`. The repository also hosts some complete [examples](https://github.com/opencost-de/opencost/tree/main/doc/examples).


## Container elements

These elements only wrap other child elements and do not directly contain data. 

| **Field name**              | **Description**                                                                                                                                                              | **Required** | **Child Elements**                                                                          | **Remarks**                                                                                                                             |
|-----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|---------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| `publication`               | Top-level element, corresponds to a single publication which costs are to be recorded for.                                                                                   | Yes          |  primary_identifier, secondary_identifiers, institutions, type, cost_data                   |                                                                                                                                         |
| `primary_identifier`        | Contains the primary identifier for the publication.                                                                                                                         | Yes          |  doi, bibliographic_information                                                             | A `doi` is strongly preferred, otherwise a `bibliographic_information` block has to be provided **instead**                             |
| `secondary_identifiers`     | Contains additional, optional identifiers.                                                                                                                                   | No           |  id                                                                                         | Element is optional, but must contain at least one child element `id` if present                                                        |
| `institution`               | Contains information to identify the paying institution.                                                                                                                     | Yes          |  id                                                                                         |                                                                                                                                         |
| `bibliographic_information` | Block of bibliographic metadata describing the publication. This serves as a backup if no `doi` can be provided.                                                             | Yes*         |  Title, Publisher, isPartOf                                                                 | Contains a subset of DC elements to identify the publication (see below). Either this **or** a `doi` have to be provided.               |
| `cost_data`                 | Aggregates all publication-related payments in form of one or more `invoice` elements                                                                                        | Yes          |  invoice                                                                                    |                                                                                                                                         |
| `invoice`                   | An `invoice` block encapsulates payment information and is meant to correspond to a real-world invoice.                                                                      | Yes          |  amount_invoice, invoice_number, amounts_paid, dates, creditor                              | Can occur more than once to handle the case of multiple invoices for a single publication.                                              |
| `dates`                     | Contains different payment-related dates                                                                                                                                     | Yes          |  date_invoice, date_paid                                                                    | At least one of the possible child elements must be given.                                                                              |
| `amounts_paid`              |                                                                                                                                                                              | Yes          |  amount_paid                                                                                |                                                                                                                                         |

## Text elements

These elements hold text data.

| **Field name**              | **Description**                                                                                                                                                                                                                                                                                                                                                        | **Type**   | **Multiple** | **Required**   | **Value Required**   | **Remarks**                                                                                                                                                                                                                                                               |
|-----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|--------------|----------------|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `doi`                       | Digital Object Identifier (DOI) to identify the publication. Serves as primary identifier.                                                                                                                                                                                                                                                                             | String     | No           | Yes*           | Yes                  |                                                                                                                                                                                                                                                                           |
| `id`                        | Secondary identifier for the publication. Possible values: `doi`, `handle`, `urn`, `isbn`, `pmid`,  `pmc`, `arxiv`, `oai`, `local`                                                                                                                                                                                                                                     | String     | Yes          | No             | No                   | Optional set of additional (persistent) identifiers. Each type may also occur more than once.                                                                                                                                                                             |
| `institution_name`          | The institution which *pays for the publication*. Possible values: `full`, `short`                                                                                                                                                                                                                                                                                     | String     | Yes          | Yes*           | Yes                  | The names are are meant to be human-readable. Either this element or `institution_id` is required.                                                                                                                                                                        |
| `institution_id`            | The institution which *pays for the publication*. Possible values: `ror`, `isni`, `ringold`                                                                                                                                                                                                                                                                            | String     | Yes          | Yes*           | Yes                  | Contains persistent identifiers for an institution. Either this element or `institution_name` is required.                                                                                                                                                                |
| `type`                      | The type of the publication described by the [COAR controlled vocabulary](https://vocabularies.coar-repositories.org/resource_types/)                                                                                                                                                                                                                                  | String     | No           | Yes            | Yes                  | This field explains the type of the publication, how the reporting institutions categorize it. Maybe this will differ from the type mentioned by  publisher, databases or elsewhere.                                                                                      |
| `external_costsplitting`    | Indicates if costs for this publication have been split with another institution. This element should only be added if there's distinct information (either positive or negative) on external cost splitting.                                                                                                                                                          | Boolean    | No           | No             | Yes                  | `1` or `true` if there's distinct information that cost splitting occured, `0` or `false` if you can confirm that it was not the case. *If unsure or there's no definite information on cost splitting, this element should be ommited*.                                  |
| `part_of_contract`          | if the publication is part of special contract e.g. [ESAC ID for transformative agreements](https://esac-initiative.org/about/transformative-agreements/agreement-registry/)                                                                                                                                                                                           | String     | No           | No             | No                   | e.g. a transformative agreement, a membership, central invoicing, community publication models etc.                                                                                                                                                                       |
| `Title`                     | Title of the publication. This is a Dublin Core Term, please refer to the corresponding definitions and comments.                                                                                                                                                                                                                                                      | string     | No           | Yes            | Yes                  | http://purl.org/dc/terms/title                                                                                                                                                                                                                                            |
| `Publisher`                 | Publisher of the journal. This is a Dublin Core Term, please refer to the corresponding definitions and comments.                                                                                                                                                                                                                                                      | string     | No           | Yes            | Yes                  | http://purl.org/dc/terms/publisher                                                                                                                                                                                                                                        |
| `isPartOf`                  | Name of the journal. This is a Dublin Core Term, please refer to the corresponding definitions and comments.                                                                                                                                                                                                                                                           | String     | No           | Yes            | Yes                  | http://purl.org/dc/terms/isPartOf                                                                                                                                                                                                                                         |
| `amount_invoice`            | Total price as stated on the invoice. A `currency` attribute is mandatory.                                                                                                                                                                                                                                                                                             | Number     | No           | No             | No                   | Net monetary value. Currency has to be a three-letter, upper case string (`EUR`, `USD` etc.) according to [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217).                                                                                                             |
| `invoice_number`            | Optional invoice number                                                                                                                                                                                                                                                                                                                                                | String     | No           | No             | No                   |                                                                                                                                                                                                                                                                           |
| `amount_paid`               | An amount paid by the institution, usually corresponding to an item on the invoice. Has 2 mandatory attributes: `currency` and `type`. `type` identifies the cost type and has to be one of `gold-oa`, `hybrid-oa`, `vat`, `colour charge`, `cover charge`, `page charge`, `permission`, `publication charge`, `reprint`, `submission fee`, `payment fee` or `other`.` | Number     | Yes          | Yes            | Yes                  | Net monetary value. For VAT use cost type VAT. Currency has to be a three-letter, uppercase string (`EUR`, `USD` etc.) according to [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217). Negative or zero values are valid to denote reimbursements or Diamond OA models.  |
| `date_paid`                 | Date of payment. Can be a certain day, month of year, or just a year.                                                                                                                                                                                                                                                                                                  | Pattern    | No           | Yes*           | Yes                  | Format: `YYYY-MM-DD`, `YYYY-MM` or `YYYY`. Either this element or `date_invoice` is required.                                                                                                                                                                             |
| `date_invoice`              | Invoice date. Can be a certain day, month of year, or just a year.                                                                                                                                                                                                                                                                                                     | Pattern    | No           | Yes*           | Yes                  | Format: `YYYY-MM-DD`, `YYYY-MM` or `YYYY`. Either this element or `date_paid` is required.                                                                                                                                                                                |
| `creditor`                  | Payment receiver as mentioned on the invoice                                                                                                                                                                                                                                                                                                                           | String     | No           | No             | Yes                  | Might not be the actual publisher, but also e.g. a service provider from another publisher                                                                                                                                                                                |


To validate your own outputs against the schema you may use:

```bash
$ xmllint --schema opencost_article.xsd myfile.xml
```

<!-- vim: spell spelllang=en_gb bomb tw=0
-->

