# openCost Metadata Schemes for Publication Cost Exchange

Scholarly publications are very well described by standardized metadata.
Existing frameworks focus on 

- bibliographic description
- legal aspects including access rights
- technical metadata like size of files etc.

However, up to know - at least to our knowledge - there exists no metadata
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

# Payments based on Individual Articles

## Global fields

| **Field name**                      | **Description**                                                                                                                       | **Type** | **Multiple** | **Required** | **Value Required** | **Remarks**                                                                                                                                                                          |
|-------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|----------|--------------|--------------|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `doi`                               | DOI to identify the publications                                                                                                      | string   | No           | Yes          | No                 | Preferably the DOI mentioned on the publication (Version of record). If no identifier exist, it has to be an empty field.                                                            |
| `id`                                | identifier of the publication. Values: `doi`, `handle`, `urn`, `isbn`, `pmid`,  `pmc`, `arxiv`, `oai`, `local`                        | String   | Yes          | No           | No                 | Specified if PID, Name or anything else                                                                                                                                              |
| `institution`                       | the institution, who pays for the  publication. This should be given also as  an open identifier preferably the ror-ID, ISNI, Ringold | String   | Yes          | Yes          | Yes                |                                                                                                                                                                                      |
| `type`                              | the type of the publication described by the [COAR controlled vocabulary](https://vocabularies.coar-repositories.org/resource_types/) | String   |              | Yes          | Yes                | This field explains the type of the publication, how the reporting institutions categorize it. Maybe this will differ from the type mentioned by  publisher, databases or elsewhere. |
| `bibliographic_information` *(TBD)* | additional information about the publication.                                                                                         | String   |              | No/Yes       | No                 | This field is mandatory if no identifier exists, otherwise it is optional. Could be structured as DC or (better) Datacite, no final decision made yet.                               |
| `oa_status`                         | status of the publication at the time of publication electronically. Values: `open`, `closed`, `hybrid`                               | String   |              | Yes          | Yes                |                                                                                                                                                                                      |
| `part_of_contract`                  | if the publication is part of special contract e.g. ESAC ID for transformative agreements                                             | String   |              | No           | No                 | e.g. a transformative agreement, a membership, central invoicing, community publication models etc.                                                                                  |


### Payment blocks

| **Field name**   | **Description**                                                                                                                                                         | **Type** | **Multiple** | **Required** | **Value Required** | **Remarks**                                                                                 |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|--------------|--------------|--------------------|---------------------------------------------------------------------------------------------|
| `amount_invoice` | price written on the invoice                                                                                                                                            | Number   |              | No           | No                 | float                                                                                       |
| `currency`       | currency identifier, mandatory attribute for all monetary amounts                                                                                                       | String   | Yes          | Yes          | Yes                | A three-letter, uppercase string (`EUR`, `USD` etc)                                         |
| `invoice_number` | number of the invoice                                                                                                                                                   | String   |              | No           | No                 |                                                                                             |
| `amount_paid`    | the actual amount paid by the institutions in the currency given                                                                                                        | Number   | Yes          | Yes          | Yes                | One entry for each payment                                                                  |
| `type`           | kind of payment values: `apc`, `hybrid-oa`, `vat`, `colour charges`, `cover`, `page charges`, `permission`, `publication charges`, `reprint`, `submission fee`, `other` | String   |              | Yes          | Yes                | controlled vocabulary                                                                       |
| `date_paid`      | date of the payment. Can be a certain day, month of year, or just a year.                                                                                               | String   |              | Yes          | Yes                | `YYYY-MM-DD`, `YYYY-MM`, `YYYY`                                                             |
| `publisher`      | name of the publisher mentioned on the invoice                                                                                                                          | String   |              | No           | No                 | might not be the actual publisher, but also e.g. a service provider from an other publisher |

To validate your own outputs against the schema you may use:

```bash
$ xmllint --schema opencost_article.xsd myfile.xml
```

<!-- vim: spell spelllang=en_gb bomb tw=0
-->

