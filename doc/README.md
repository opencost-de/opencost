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
    |--- institutions
    |       |
    |       |--- institution type=ror
    |       |--- institution type=short_name
    |
    |--- type
    |--- oa_status
    |--- amounts_paid
    |     |
    |     |--- item
    |     |      |
    |     |      |--- amount_invoice
    |     |      |--- date_paid
    |     |      |--- publisher
    |     |      |--- invoice_number
    |     |      |--- amounts_paid
    |     |             |
    |     |             |--- amount_paid
    |     |             |--- amount_paid
    |     |
    |     |--- item
    |
    |--- (part of contract)
```

In XML we use the namespace `opencost`. The repository also hosts some complete [examples](https://github.com/opencost-de/opencost/tree/main/doc/examples).


## First-level elements

| **Field name**              | **Description**                                                                                                                                                              | **Type**   | **Multiple** | **Required** | **Value Required** | **Remarks**                                                                                                                                                                          |
|-----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|--------------|--------------|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `doi`                       | DOI to identify the publication. Primary identifier.                                                                                                                         | string     | No           | Yes*         | No                 | Preferably the DOI mentioned on the publication (Version of record). Either this **or** a `bibliographic_information` have to be provided.                                           |
| `bibliographic_information` | Block of bibliographic metadata describing the publication. This serves as a backup if no `doi` can be provided.                                                             | Subelement | No           | Yes*         | No                 | Contains a subset of DC elements to identify the publication (see below). Either this **or** a `doi` have to be provided.                                                            |
| `id`                        | Secondary identifiers for the publication. Possible values: `doi`, `handle`, `urn`, `isbn`, `pmid`,  `pmc`, `arxiv`, `oai`, `local`                                          | String     | Yes          | No           | No                 | Optional set of additional (persistent) identifiers. Each type may also occur more than once.                                                                                        |
| `institution`               | The institution which *pays for the publication*. Possible values: `ror`, `isni`, `ringold`, `full_name`, `short_name`                                                       | String     | Yes          | Yes          | Yes                | `full_name` and `short_name` are meant to be human-readable names                                                                                                                    |
| `type`                      | The type of the publication described by the [COAR controlled vocabulary](https://vocabularies.coar-repositories.org/resource_types/)                                        | String     |              | Yes          | Yes                | This field explains the type of the publication, how the reporting institutions categorize it. Maybe this will differ from the type mentioned by  publisher, databases or elsewhere. |
| `oa_status`                 | Status of the publication at the time of its electronic publication. Possible values: `open`, `closed`, `hybrid`                                                             | String     |              | Yes          | Yes                |                                                                                                                                                                                      |
| `item`                      | An `item` block encapsulates payment information and is meant to correspond to a real-world invoice.                                                                         | Subelement | Yes          | Yes          | Yes                | Can occur more than once to handle the case of multiple invoices for a single publication.                                                                                           |
| `part_of_contract`          | if the publication is part of special contract e.g. [ESAC ID for transformative agreements](https://esac-initiative.org/about/transformative-agreements/agreement-registry/) | String     |              | No           | No                 | e.g. a transformative agreement, a membership, central invoicing, community publication models etc.                                                                                  |

<!-- TODO
- `item` is a second level element, the first level would be the outer `amounts_paid`
- we have two nested `amounts_paid` which is not nice
-->

## Second-level elements

### bibliographic_information

DRAFT: 

| **Field name**  | **Description**                                                                                                            | **Type**   | **Multiple**   | **Required**   | **Value Required**   | **Remarks**                                  |
|-----------------|----------------------------------------------------------------------------------------------------------------------------|------------|----------------|----------------|----------------------|----------------------------------------------|
| `Title`         | Title of the publication. This is a Dublin Core Term, please refer to the corresponding definitions and comments.          | string     | No             | Yes            | Yes                  | http://purl.org/dc/terms/title               |
| `Publisher`     | Publisher of the journal. This is a Dublin Core Term, please refer to the corresponding definitions and comments.          | string     | No             | Yes            | Yes                  | http://purl.org/dc/terms/publisher           |
| `isPartOf`      | Name of the journal. This is a Dublin Core Term, please refer to the corresponding definitions and comments.               | String     | No             | Yes            | Yes                  | http://purl.org/dc/terms/isPartOf            |


### item

| **Field name**   | **Description**                                                                                                                                                                                                                                                                                                                                 | **Type** | **Multiple** | **Required** | **Value Required** | **Remarks**                                                                                                                                                                              |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|--------------|--------------|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `amount_invoice` | Total price as stated on the invoice. A `currency` attribute is mandatory.                                                                                                                                                                                                                                                                      | Number   | No           | No           | No                 | Net monetary value. Currency has to be a three-letter, upper case string (`EUR`, `USD` etc.) according to [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217).                            |
| `invoice_number` | Optional invoice number                                                                                                                                                                                                                                                                                                                         | String   | No           | No           | No                 |                                                                                                                                                                                          |
| `amount_paid`    | An amount paid by the institution, usually corresponding to an item on the invoice. Has 2 mandatory attributes: `currency` and `type`. `type` identifies the cost type and has to be one of `apc`, `hybrid-oa`, `vat`, `colour charges`, `cover`, `page charges`, `permission`, `publication charges`, `reprint`, `submission fee` or `other`.` | Number   | Yes          | Yes          | Yes                | Net monetary value. For VAT use cost type VAT. Currency has to be a three-letter, uppercase string (`EUR`, `USD` etc.) according to [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217).  |
| `date_paid`      | Date of payment. Can be a certain day, month of year, or just a year.                                                                                                                                                                                                                                                                           | String   |              | Yes          | Yes                | Format: `YYYY-MM-DD`, `YYYY-MM` or `YYYY`                                                                                                                                                |
| `publisher`      | Name of the publisher mentioned on the invoice                                                                                                                                                                                                                                                                                                  | String   |              | No           | No                 | Might not be the actual publisher, but also e.g. a service provider from another publisher                                                                                               |

<!-- TODO
- `publisher` is actually the recipient of the invoice. Field name?
-->

To validate your own outputs against the schema you may use:

```bash
$ xmllint --schema opencost_article.xsd myfile.xml
```

<!-- vim: spell spelllang=en_gb bomb tw=0
-->

