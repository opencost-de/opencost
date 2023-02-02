# openCost Metadata Schemes for Publication Cost Exchange

Scholarly publications are very well described by standardized metadata.
Existing frameworks focus on 

- bibliographic description
- legal aspects including access rights
- technical metadata like size of files etc.

However, up to know - at least to our knowledge - there exists no meta data
schema to describe _financial_ aspects of publications. On the other hand
_transparency_ for costs is imperative for the transformation of scholarly
publishing to Open Access (OA) if one wants to avoid ever increasing costs.

In collaboration with a lot of stakeholder and close interaction with the
community our goal is to develop schemes for payment data to fill this gap.
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
the scheme to your payment, ask about any doubts, and are invited to upload
further examples.

Let's start the discussion!

# Payments based on Individual Articles

## Global fields

| **Field name**                 | **Description**                                                                              | **Type** | **Multiple** | **Required** | **Value Required** | **Remarks**                              |
|--------------------------------|----------------------------------------------------------------------------------------------|----------|--------------|--------------|--------------------|------------------------------------------|
| `doi`                          | DOI to identify the publications                                                             | string   | No           | Yes          | No                 | Preferably the DOI mentioned on the      |
|                                |                                                                                              |          |              |              |                    | publication (Version of record). If no   |
|                                |                                                                                              |          |              |              |                    | identifier exist, it has to be an empty  |
|                                |                                                                                              |          |              |              |                    | field.                                   |
| `id`                           | identifier of the publication. This can                                                      | String   | Yes          | No           | No                 |                                          |
|                                | be a `doi`, `handle`, `urn`, `isbn`, `pmid`,                                                 |          |              |              |                    |                                          |
|                                | `pmc`, `arxiv`, `oai`, `local`                                                               |          |              |              |                    |                                          |
| `institution`                  | the institution, who pays for the                                                            | String   | Yes          | Yes          | Yes                | Specified if PID, Name or anything else  |
|                                | publication. This should be given also as                                                    |          |              |              |                    |                                          |
|                                | an open identifier preferably the                                                            |          |              |              |                    |                                          |
|                                | ror-ID, ISNI, Ringold                                                                        |          |              |              |                    |                                          |
| `type`                         | the type of the publication described by                                                     | String   |              | Yes          | Yes                | This field explains the type of the      |
|                                | the [COAR controlled vocabulary](https://vocabularies.coar-repositories.org/resource_types/) |          |              |              |                    | publication, how the reporting           |
|                                |                                                                                              |          |              |              |                    | institutions categorize it. Maybe this   |
|                                |                                                                                              |          |              |              |                    | will differ from the type mentioned by   |
|                                |                                                                                              |          |              |              |                    | publisher, databases or elsewhere.       |
| `bibliographic_information`    | information about the publication.                                                           | String   |              | No/Yes       | No                 | This field is mandatory if no identifier |
|                                |                                                                                              |          |              |              |                    | exists, otherwise it is optional.        |
|                                |                                                                                              |          |              |              |                    | Structured as DC or (better) Datacite    |
| `oa_status_orig`               | status of the publication at the time of                                                     | String   |              | Yes          | Yes                | Values:                                  |
|                                | publication electronically                                                                   |          |              |              |                    |                                          |
|                                |                                                                                              |          |              |              |                    | open, closed, hybrid                     |
| `part_of_contract`             | if the publication is part of special                                                        | String   |              | No           | No                 | e.g. a transformative agreement, a       |
|                                | contract                                                                                     |          |              |              |                    | membership, central invoicing, community |
|                                |                                                                                              |          |              |              |                    | publication models etc.                  |
|                                |                                                                                              |          |              |              |                    |                                          |
|                                |                                                                                              |          |              |              |                    | Maybe the ESAC registry ID               |


### Payment blocks

| **Field name**                 | **Description**                                                                              | **Type** | **Multiple** | **Required** | **Value Required** | **Remarks**                              |
|--------------------------------|----------------------------------------------------------------------------------------------|----------|--------------|--------------|--------------------|------------------------------------------|
| `amount_invoice`               | price written on the invoice in the given                                                    | Number   |              | No           | No                 | float                                    |
|                                | currency                                                                                     |          |              |              |                    |                                          |
| `invoice_number`               | number of the invoice                                                                        | String   |              | No           | No                 |                                          |
| `amount_paid`                  | the actual amount paid by the                                                                | Number   |              | Yes          | Yes                | One entry for each payment, can be       |
|                                | institutions in the currency                                                                 |          |              |              |                    | repeated, e.g. payment of APC and VAT    |
| `type`                         | what kind of payment                                                                         | String   |              | Yes          | Yes                | e.g. colour charges, pagecharges, apc,   |
|                                | Values: `apc`, `hybrid-oa`, `colour charges`, `cover`, `page charges`, `permission`          |          |              |              |                    | bpc, cover charge, controlled vocabulary |
|                                | `publication charges`, `reprint`, `submission fee`                                           |          |              |              |                    | bpc, cover charge, controlled vocabulary |
| `date_paid`                    | date of the payment                                                                          | String   |              | Yes          | Yes                | `YYYY-MM-DD`                             |
|                                |                                                                                              |          |              |              |                    |                                          |
|                                |                                                                                              |          |              |              |                    | Recommended exact day.                   |
|                                |                                                                                              |          |              |              |                    | Minimal resolution: year                 |
|                                |                                                                                              |          |              |              |                    |                                          |
| `publisher`                    | name of the publisher mentioned at the                                                       | String   |              | No           | No                 | might not be the actual publisher, where |
|                                | invoice                                                                                      |          |              |              |                    | the publication is published, e.g.       |
|                                |                                                                                              |          |              |              |                    | service from an other publisher          |

To validate your own outputs against the schema you may use:

```bash
$ xmllint --schema opencost_article.xsd myfile.xml
```

<!-- vim: spell spelllang=en_gb bomb tw=0
-->

