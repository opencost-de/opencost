# openCost Metadata Schemas for Publication Cost Exchange

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

Here we introduce our meta data schemas for further discussion. You can compare
the schema to your payment, ask about any doubts, and are invited to upload
further examples.

In XML we use the namespace `opencost`. The repository also hosts some complete [examples](https://github.com/opencost-de/opencost/tree/main/doc/examples).

## Metadata Schema: Overview

- All XML elements can be either classified as container elements or text elements. Container elements only wrap other elements and do not directly contain data. Text elements hold the actual data.
- Empty elements are not allowed: Whenever an element is indicated to be required, it has to contain either another element or text.
- The schema does not make use of XML attributes, type/value element combinations are used instead. This is a deliberate decision to make the schema easily exportable to other formats like JSON.
- There are two main entities defined in the schema: `publication`, representing a journal article and its associated (cost) metadata, and `contract`, containing data related to payment models like transformative agreements, association memberships or subscriptions.
. The top element in the schema is `opencost:data`, which may contain an arbitrary combination of `publication` and `contract` elements.
- The two main entities are decribed below, both in a tree-like overview and a more detailed table. Table entries are linked to tree elements via an identification number.
- In the table, the `Required` column describes if an element is mandatory. `No` indicates that the element is optional, `Yes` marks required elements. Note however that the `Yes` status only relates to an element's direct parent: If the higher-level element does not exist for whatever reason, the child can also be left out even if marked as required. The third option is `choice`: This indicates that the element can be omitted if another element on the same level is given instead. Have a look at the `Description/Remarks` column to find out which elements form a `choice` relation.
- The `Repeatable` column indicates if an element may occur more than once.
- `publication` elements may be linked to `contract` elements to model relations like an article being paid for centrally under a non-APC payment model. This is done semantically by adding `part_of_contract` to a `publication` element's `cost_data` block and defining a `group_id` within. The `group_id` is then repeated within a `contract` element's `invoice_group`, effectively linking a publication to a set of invoices. The `group_id` may be chosen freely, however we recommend to use a unique identifier which is unlikely to reappear for other data providers within large collections. A possible approach is to use a combination of the institution's ROR ID, the contract primary identifier and a year.

## Data schema for individual articles (`opencost:publication`)

The overall tree structure looks like this:
```
publication [1]
    |
    |--- primary_identifier [2]
    |     |
    |     |--- doi [2.1]          
    |     |
    |	  | *either doi OR bibliographic_information!*
    |     |
    |     | --- bibliographic_information [2.2]
    |              |
    |              |--- Title [2.2.1]
    |              |--- Publisher [2.2.2]
    |              |--- isPartOf [2.2.3]
    |
    |--- secondary_identifiers [3]                                            
    |     |
    |     |--- id [3.1]                                                      
    |     |     |
    |     |     |--- type = doi / handle / urn / isbn / pmid / pmc / arxiv / oai / local [3.1.1]  
    |     |     |--- value [3.1.2] 
    |     |
    |     |--- id                                                      
    |           |
    |           |--- [...]         
    |           
    |--- institution [4]
    |     |
    |     |--- id [4.1]                                                        
    |     |     |
    |     |     |--- type = ror / isni / ringold [4.1.1]               
    |     |     |--- value [4.1.2]
    |     |      
    |     |--- name [4.2]
    |           |
    |           |--- type = full / short [4.2.1]
    |           |--- value [4.2.2]
    |       
    |--- publication_type = COAR controlled vocabulary [5]                   
    |  
    |--- external_costsplitting = true _OR_ 1 / false _OR_ 0 [6]                  
    |  
    |--- cost_data [7]
    |     |
    |     |--- part_of_contract [7.1]
    |     |     |
    |     |     |--- primary_identifier [7.1.1]
    |     |     |     |
    |     |     |     |--- type = ESAC [7.1.1.1]
    |     |     |     |--- value [7.1.1.2]
    |     |     |
    |     |     |---	group_id [7.1.2]                                         
    |     |
    |     |--- invoice [7.2]
    |     |     |
    |     |     |--- invoice_number [7.2.1]
    |     |     |                                        
    |     |     |--- creditor [7.2.2]
    |     |     |
    |     |     |--- dates [7.2.3]                                                
    |     |     |     |
    |     |     |     |--- invoice [7.2.3.1]
    |     |     |     |--- paid [7.2.3.2]
    |     |     |
    |     |     |--- amount_invoice [7.2.4]                                        
    |     |     |     |
    |     |     |     |--- amount [7.2.4.1]
    |     |     |     |--- currency [7.2.4.2]
    |     |     |
    |     |     |--- amounts_paid [7.2.5]                                        
    |     |           |
    |     |           |--- amount_paid [7.2.5.1]
    |     |           |
    |     |           |     |--- amount [7.2.5.1.1]
    |     |           |     |--- currency [7.2.5.1.2]
    |     |           |     |--- cost_type [7.2.5.1.3]
    |     |           |
    |     |           |--- amount_paid
    |     |                 |
    |     |                 |--- [...]
    |     |
    |     |--- invoice
    |           |
    |           |--- [...]
    |
```


| No        | Field name                  | Values                                                                                                                                                                                                                 | Data Type   | Repeatable | Required  | Description/Remarks                                                                                                                                                                                                                                                                                     |
|:----------|:----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1         | `publication`               |                                                                                                                                                                                                                        |             | Yes      | Yes       | Top-level element, corresponds to a single publication for which costs are to be recorded.                                                                                                                                                                                                              |
| 2         | `primary_identifier`        |                                                                                                                                                                                                                        |             | No       | Yes       | Contains the primary identifier for the publication. A `doi` is strongly preferred, otherwise a `bibliographic_information` block has to be provided instead.                                                                                                                                               |
| 2.1       | `doi`                       |                                                                                                                                                                                                                        | String      | No       | Choice    | Digital Object Identifier (doi) to identify the publication. Serves as primary identifier.                                                                                                                                                                                                              |
| 2.2       | `bibliographic_information` |                                                                                                                                                                                                                        |             | No       | Choice    | Block of bibliographic metadata describing the publication. This serves as a backup and only has to be given if no `doi` can be provided. Contains a subset of DC elements to identify the publication (see below).                                                                                       |
| 2.2.1     | `Title`                     | [This is a Dublin Core Term, please refer to the corresponding definitions and comments.](http://purl.org/dc/terms/title)                                                                                              | String      | No       | Yes       | Title of the publication.                                                    |
| 2.2.2     | `Publisher`                 | [This is a Dublin Core Term, please refer to the corresponding definitions and comments.](http://purl.org/dc/terms/publisher)                                                                                          | String      | No       | Yes       | Publisher of the journal.          |
| 2.2.3     | `isPartOf`                  | [This is a Dublin Core Term, please refer to the corresponding definitions and comments.](http://purl.org/dc/terms/isPartOf)                                                                                           | String      | No       | Yes       | Name of the journal.                                                         |
| 3         | `secondary_identifiers`     |                                                                                                                                                                                                                        |             | No       | No        | Contains additional, optional identifiers. Element is optional, but must contain at least one child element `id` if present.                                                                                                                                                                              |
| 3.1       | `id`                        |                                                                                                                                                                                                                        |             | Yes      | No        | Secondary identifier for the publication. Optional set of additional (persistent) identifiers. Each type may also occur more than once.                                                                                                                                                                 |
| 3.1.1     | `type`                      | Possible values: `doi`, `handle`, `urn`, `isbn`, `pmid`, `pmc`, `arxiv`, `oai`, `local`                                                                                                                                | Enumeration | No       | Yes       |                                                                                                                                                                  |
| 3.1.2     | `value`                     |                                                                                                                                                                                                                        | String      | No       | Yes       |                                                                                                                                                                 |
| 4         | `institution`               |                                                                                                                                                                                                                        |             | No       | Yes       | Contains information to identify the paying institution.                                                                                                                                                                                                                                                |
| 4.1       | `id`                        |                                                                                                                                                                                                                        |             | Yes      | Choice    | Defines the institution which pays for the publication. Contains persistent identifiers for an institution. Either this element or the institution's `name` is required.      |
| 4.1.1     | `type`                      | Possible values: `ror`, `isni`, `ringold`                                                                                                                                                                              | Enumeration | Yes      | Yes       |
| 4.1.2     | `value`                     |                                                                                                                                                                                                                        | String      | Yes      | Yes       |       |
| 4.2       | `name`                      |                                                                                                                                                                                                                        |             | Yes      | Choice    | Defines the institution which pays for the publication. The names are meant to be human-readable. Either this element or the institution's `id` is required.                                                                                                                                                |
| 4.2.1     | `type`                      | Possible values: `full`, `short`                                                                                                                                                                                       | Enumeration | Yes      | Yes     |                                                                                                                                     |
| 4.2.2     | `value`                     |                                                                                                                                                                                                                        | String      | Yes      | Yes     |                                                                                                                                |
| 5         | `publication_type`          | Possible values: [COAR controlled vocabulary](https://vocabularies.coar-repositories.org/resource_types/)                                                                                                              | Enumeration | No       | Yes       | This field explains the type of the publication, how the reporting institutions categorize it. Maybe this will differ from the publication type mentioned by publisher, databases or elsewhere.                                                                                                         |
| 6         | `external_costsplitting`    |`1` or `true` = distinct information that cost splitting occured, `0` or `false` = to confirm that it was not the case. If unsure or there’s no definite information on cost splitting, this element should be omitted. | Boolean     | No       | No        | Yes            | Indicates if costs for this publication have been split with another institution. This element should only be added if there’s distinct information (either positive or negative) on external costsplitting.                                                                                           |
| 7         | `cost_data`                 |                                                                                                                                                                                                                        |             | No       | Yes       | Aggregates all publication-related payments in form of one or more `invoice` elements. May also refer to a transformative agreement via a `part_of_contract` element. Permitted to contain at most one `part_of_contract` and an arbitrary number of `invoice` elements. At least one element must be provided. |
| 7.1       | `part_of_contract`          |                                                                                                                                                                                                                        |             | No       | Choice        | Contains identifiers to link this publication to a contract. Providing just a `primary_identifier` is possibe to denote that a publication belongs to a contract but was still paid for individually.                                                                                                     |
| 7.1.1     | `primary_identifier`        |                                                                                                                                                                                                                        |             | No       | Yes        | Identical to the `primary_identifier` of an `opencost:contract` and indicates that the article was published under that contract.                                                                                                                                                                           |
| 7.1.1.1   | `type`                      | Possible values: [`ESAC`](https://esac-initiative.org/about/transformative-agreements/agreement-registry/)                                                                                                             | Enumeration | No       | Yes        |                                                                                                                                                                       |
| 7.1.1.2   | `value`                     |                                                                                                                                                                                                                        | String      | No       | Yes        |                                                                                                                                                                            |
| 7.1.2     | `group_id`                  | Generating a [`uuid`](https://generateuuid.online/) or using another type of unique identifier is recommended.                                                                                                         | String      | No       | No        | Identical to the `group_id` of an `opencost:contract//opencost:cost_data//opencost:invoice_group` element. Indicates that publication costs relate to that particular `invoice_group` within a defined accounting period of a contract. Can be omitted to just link a publication to a certain contract.      |
| 7.2       | `invoice`                   |                                                                                                                                                                                                                        |             | Yes      | Choice       | An `invoice` block encapsulates payment information and is meant to correspond to a real-world invoice. Can occur more than once to handle the case of multiple invoices for a single publication.                                                                                                        |
| 7.2.1     | `invoice_number`            | As mentioned on the invoice.                                                                                                                                                                                           | String      | No       | No        | Optional invoice number.                                                                                                                                                                                                                                                                                 |
| 7.2.2     | `creditor`                  | As mentioned on the invoice.                                                                                                                                                                                           | String      | No       | No        | Payment receiver. Might not be the actual publisher, but also e.g. a service provider from another publisher.                                                                                                                                                                                                 |
| 7.2.3     | `dates`                     |                                                                                                                                                                                                                        |             | No       | Yes       | Contains different payment-related dates. At least one of the possible child elements, date `invoice` or `paid`, must be given.                                                                                                                                                                             |
| 7.2.3.1   | `invoice`                   | Format: `YYYY-MM-DD`, `YYYY-MM` or `YYYY`                                                                                                                                                                              | Pattern     | No       | Choice     | Invoice date. Can be a certain day, month of year, or just a year. Either this element or date paid is required.                                                                                                                                                                                        |
| 7.2.3.2   | `paid`                      | Format: `YYYY-MM-DD`, `YYYY-MM` or `YYYY`                                                                                                                                                                              | Pattern     | No       | Choice     | Date of payment. Can be a certain day, month of year, or just a year. Either this element or the invoice date is required.                                                                                                                                                                               |
| 7.2.4     | `amount_invoice`            |                                                                                                                                                                                                                        |             | No       | No        | Contains the total price as stated on the invoice by specifying the child elements `amount` and `currency`.                                                                                                                                                                                                     |
| 7.2.4.1   | `amount`                    | Net monetary value.                                                                                                                                                                                                    | Number      | No       | Yes        | Total amount as stated on the invoice.                                                                                                                                                                                                                                                                  |
| 7.2.4.2   | `currency`                  | Currency has to be a three-letter, upper case string (`EUR`, `USD` etc.) according to [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217).                                                                              | Pattern     | No       | Yes        | Currency of the total amount as stated on the invoice.                                                                                                                                                                                                                                                  |
| 7.2.5     | `amounts_paid`              |                                                                                                                                                                                                                        |             | No       | Yes        | Contains all itemized amounts paid corresponding to one invoice.                                                                                                                                                                                                                                        |
| 7.2.5.1   | `amount_paid`               |                                                                                                                                                                                                                        |             | Yes      | Yes       | A single amount paid by the institution, usually corresponding to an item on the invoice. Is defined by the child elements `amount`, `currency` and `cost_type`.                                                                                                                                              |
| 7.2.5.1.1 | `amount`                    | Net monetary value. Negative or zero values are valid to denote reimbursements or Diamond OA models.                                                                                                                   | Number      | No       | Yes       | Amount of the `cost_type`.                                                                                                                                                                                                                                                                                 |
| 7.2.5.1.2 | `currency`                  | Currency has to be a three-letter, upper case string (`EUR`, `USD` etc.) according to [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217).                                                                              | Pattern     | No       | Yes       | Currency of the `cost_type`.                                                                                                                                                                                                                                                                              |
| 7.2.5.1.3 | `cost_type`                 | Possible values: `gold-oa`, `hybrid-oa`, `vat`, `colour charge`, `cover charge`, `page charge`, `permission`, `publication charge`, `reprint`, `submission fee`, `payment fee` or `other`.                             | Enumeration | No       | Yes       | `cost_type` describes the object/purpose of the payment.                                                                                                                                                                                                                                                       |




## Data schema for contracts/transformative agreements (`opencost:contract`)

```
contract [1]
    |
    |--- contract_name [2]
    |
    |--- institution [3]
    |     |
    |     |--- id [3.1]
    |     |     |
    |     |     |--- type = ror / isni / ringold [3.1.1]              
    |     |     |--- value [3.1.2]
    |     |      
    |     |--- name [3.2]
    |           |
    |           |--- type = full / short [3.2.1]
    |           |--- value [3.2.2]
    |       
    |--- participation [4]
    |     |
    |     |--- from [4.1]
    |     |--- to [4.2]
    |
    |--- primary_identifier [5]
    |     |
    |     |--- type = ESAC [5.1]
    |     |--- value [5.2]
    |
    |--- secondary_identifiers [6]
    |     |
    |     |--- id [6.1]
    |     |     |
    |     |     |--- type = oai, ezb, local [6.1.1]
    |     |     |--- value [6.1.2]
    |     |
    |     |--- id
    |     |     |--- [...]
    |
    |--- cost_data [7]
    |     |
    |     |--- invoice_group [7.1]
    |     |     |
    |     |     |--- group_id [7.1.1]
    |     |     |    
    |     |     |--- invoices_period [7.1.2]
    |     |     |     |
    |     |     |     |--- from [7.1.2.1]
    |     |     |     |--- to [7.1.2.2]
    |     |     |
    |     |     |--- invoice [7.1.3]
    |     |     |     |
    |     |     |     |--- invoice_number [7.1.3.1]
    |     |     |     |                              
    |     |     |     |--- creditor [7.1.3.2]
    |     |     |     |
    |     |     |     |--- dates [7.1.3.3]
    |     |     |     |     |
    |     |     |     |     |--- invoice [7.1.3.3.1]
    |     |     |     |     |--- paid [7.1.3.3.2]
    |     |     |     |
    |     |     |     |--- amount_invoice [7.1.3.4]
    |     |     |     |     |
    |     |     |     |     |--- amount [7.1.3.4.1]
    |     |     |     |     |--- currency [7.1.3.4.2]
    |     |     |     |
    |     |     |     |--- amounts_paid [7.1.3.5]
    |     |     |     |     |
    |     |     |     |     |--- amount_paid [7.1.3.5.1]
    |     |     |     |     |     |
    |     |     |     |     |     |--- amount [7.1.3.5.1.1]
    |     |     |     |     |     |--- currency [7.1.3.5.1.2]
    |     |     |     |     |     |--- cost_type [7.1.3.5.1.3]
    |     |     |     |     |
    |     |     |     |     |--- amount_paid
    |     |     |     |     |     |
    |     |     |     |     |     |--- [...]
    |     |     |
    |     |     |--- invoice
    |     |     |     |
    |     |     |     |--- [...]
    |     |
    |     |--- invoice_group
    |     |     |
    |     |     |--- [...]
    |
```

| No.         | Field name              | Values                                                                                                                                     | Data Type   | Repeatable | Required | Description/Remarks                                                                                                                                                                                                                                                                                                                                                         |
|:------------|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|-------------|------------|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1           | `contract`              |                                                                                                                                            |             | Yes      | Yes      | Top-level element, corresponds to a contract (e. g. transformative agreements and memberships) for which costs are to be recorded.                                                                                                                                                                                                                                          |
| 2           | `contract_name`         |                                                                                                                                            | String      | No       | Yes      | A human-readable label for the contract.                                                                                                                                                                                                                                                                                                                                    |
| 3           | `institution`           |                                                                                                                                            |             | No       | Yes      | Contains information to identify the institution taking part in the contract.                                                                                                                                                                                                                                                                                               |
| 3.1         | `id`                    |                                                                                                                                            |             | Yes      | Choice   | Defines the institution which takes part in the contract. Contains persistent identifiers for an institution. Either this element or the institution's `name` is required.                                                                                                                                                                                                  |
| 3.1.1       | `type`                  | Possible values: `ror`, `isni`, `ringold`.                                                                                                 | Enumeration | No       | Yes	     |                                                                                                                                                                                                  |
| 3.1.2       | `value`                 |                                                                                                                                            | String      | No       | Yes      |                                                                                                                                                                                                    |
| 3.2         | `name`                  |                                                                                                                                            |             | Yes      | Choice   | Defines the institution which takes part in the contract. The names are meant to be human-readable. Either this element or the institution's `id` is required.                                                                                                                                                                                                              |
| 3.2.1       | `type`                  | Possible values: `full`, `short`.                                                                                                          | Enumeration | No       | Yes      |                                                                                                                                                                                                              |
| 3.2.2       | `value`                 |                                                                                                                                            | String      | No       | Yes      |                                                                                                                                                                                                             |
| 4           | `participation`         |                                                                                                                                            |             | No       | Yes      | Contains information on the dates an institution joined and left a contract.                                                                                                                                                                                                                                                                                                |
| 4.1         | `from`                  | Format: `YYYY-MM-DD`, `YYYY-MM` or `YYYY`                                                                                                  | Pattern     | No       | Yes      | The date when the institution joined the contract. Not to be confused with the start date of the agreement itself, which may be earlier.                                                                                                                                                                                                                                    |
| 4.2         | `to`                    | Format: `YYYY-MM-DD`, `YYYY-MM` or `YYYY`                                                                                                  | Pattern     | No       | Yes      | The date when the institution left the contract. Not to be confused with the end date of the agreement itself, which may be later.                                                                                                                                                                                                                                          |
| 5           | `primary_identifier`    |                                                                                                                                            |             | No       | Yes      | Persistent, global identifier for the contract. Currently only an [`ESAC` ID](https://esac-initiative.org/about/transformative-agreements/agreement-registry/) is accepted.                                                                                                                                                                                                 |
| 5.1         | `type`                  | Possible value: `ESAC`                                                                                                                     | Enumeration | No       | Yes      |                                                                                                                                                                                                  |
| 5.2         | `value`                 |                                                                                                                                            | String      | No       | Yes      |                                                                                                                                                                                                |
| 6           | `secondary_identifiers` |                                                                                                                                            |             | No       | No       | Contains additional, optional identifiers for the contract. Element is optional, but must contain at least one child element `id` if present.                                                                                                                                                                                                                               |
| 6.1         | `id`                    |                                                                                                                                            |             | Yes      | Yes      | Secondary identifier for the contract. Use optional set of additional (persistent) identifiers. Each type may occur more than once.                                                                                                                                                                                                                                         |
| 6.1.1       | `type`                  | Possible values: `oai`, `ezb`, `local`.                                                                                                    | Enumeration | No       | Yes      |                                                                                                                                                                                                                                    |
| 6.1.2       | `value`                 |                                                                                                                                            | String      | No       | Yes      |                                                                                                                                                                                                                                       |
| 7           | `cost_data`             |                                                                                                                                            |             | No       | Yes      | Aggregates payments related to a contract, in form of one or more `invoice` elements. These `invoice` elements can be combined into one or more common `invoice_group` elements referring to a shared `invoices_period` of the contract concerned.                                                                                                                          |
| 7.1         | `invoice_group`         |                                                                                                                                            |             | Yes      | Yes      | Contains all invoices that belong to a billing period within a contract. Such a contract phase is limited by a time period (`invoices_period`) to which a respective invoice can be assigned.                                                                                                                                                                               |
| 7.1.1       | `group_id`              | Generating a [`uuid`](https://generateuuid.online/) or using another type of unique identifier is recommended.                             | String      | No       | Yes      | The `group_id` is an id to uniquely name and identify the `invoice_group`. Naming a `group_id` is necessary to link not only from an individual publication to the global contract but also to a specific invoice and contract period: Can be used to relate cost data for an `opencost:publication` to a certain contract via the `opencost:part_of_contract` element.     |
| 7.1.2       | `invoices_period`       |                                                                                                                                            |             | No       | Yes      | Identifies the time frame an invoice refers to.                                                                                                                                                                                                                                                                                                                             |
| 7.1.2.1     | `from`                  | Format: `YYYY-MM-DD`, `YYYY-MM` or `YYYY`.                                                                                                 | Pattern     | No       | Yes      | Start date of the time frame the invoice refers to. Can be different to an institution’s contract accession (`participation // from`) if multiple invoices have been issued over the total contract duration.                                                                                                                                                               |
| 7.1.2.2     | `to`                    | Format: `YYYY-MM-DD`, `YYYY-MM` or `YYYY`.                                                                                                 | Pattern     | No       | Yes      | End date of the time frame the invoice refers to. Can be different to an institution’s contract termination (`participation // to`) if multiple invoices have been issued over the total contract duration.                                                                                                                                                                 |
| 7.1.3       | `invoice`               |                                                                                                                                            |             | Yes      | Yes      | An `invoice` block encapsulates payment information for a contract and is meant to correspond to a real-world invoice. Can occur more than once to handle the case of multiple invoices for a single contract.                                                                                                                                                              |
| 7.1.3.1     | `invoice_number`        | As mentioned on the invoice.                                                                                                               | String      | No       | No       | Optional invoice number.                                                                                                                                                                                                                                                                                                                                                    |
| 7.1.3.2     | `creditor`              | As mentioned on the invoice.                                                                                                               | String      | No       | No       | Payment receiver as mentioned on the invoice. Might not be the actual publisher, but also a service provider.                                                                                                                                                                                                                                                               |
| 7.1.3.3     | `dates`                 |                                                                                                                                            |             | No       | Yes      | Contains different payment-related dates. At least one of the possible child elements, date `invoice` or `paid`, must be given.                                                                                                                                                                                                                                             |
| 7.1.3.3.1   | `invoice`               | Format: `YYYY-MM-DD`, `YYYY-MM` or `YYYY`                                                                                                  | Pattern     | No       | Choice   | Invoice date. Can be a certain day, month of year, or just a year. Either this element or the date `paid` is required.                                                                                                                                                                                                                                                      |
| 7.1.3.3.2   | `paid`                  | Format: `YYYY-MM-DD`, `YYYY-MM` or `YYYY`                                                                                                  | Pattern     | No       | Choice   | Date of payment. Can be a certain day, month of year, or just a year. Either this element or the `invoice` date is required.                                                                                                                                                                                                                                                |
| 7.1.3.4     | `amount_invoice`        |                                                                                                                                            |             | No       | No       | Contains the total price as stated on the invoice for the contract by specifying the child elements `amount` and `currency`.                                                                                                                                                                                                                                                |
| 7.1.3.4.1   | `amount`                | Net monetary value.                                                                                                                        | Number      | No       | No       | Total amount as stated on the invoice for the contract.                                                                                                                                                                                                                                                                                                                     |
| 7.1.3.4.2   | `currency`              | Currency has to be a three-letter, upper case string (`EUR`, `USD` etc.) according to [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217).  | Pattern     | No       | No       | Currency of the total amount as stated on the invoice for the contract.                                                                                                                                                                                                                                                                                                     |
| 7.1.3.5     | `amounts_paid`          |                                                                                                                                            |             | No       | Yes      | Contains all itemized amounts paid corresponding to one invoice of a contract.                                                                                                                                                                                                                                                                                              |
| 7.1.3.5.1   | `amount_paid`           |                                                                                                                                            |             | Yes      | Yes      | An amount paid by the institution, usually corresponding to an item on the invoice. Is defined by the child elements `amount`, `currency` and `cost_type`.                                                                                                                                                                                                                  |
| 7.1.3.5.1.1 | `amount`                | Net monetary value. Negative or zero values are valid to denote reimbursements.                                                            | Number      | No       | Yes      | Amount of the `cost_type`.                                                                                                                                                                                                                                                                                                                                                  |
| 7.1.3.5.1.2 | `currency`              | Currency has to be a three-letter, upper case string (`EUR`, `USD` etc.) according to [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217).  | Pattern     | No       | Yes      | Currency of the `cost_type`.                                                                                                                                                                                                                                                                                                                                                |
| 7.1.3.5.1.3 | `cost_type`             | Possible values: `publish`, `read` or `vat`                                                                                                | Enumeration | No       | Yes      | cost_type describes the object/purpose of the payment.                                                                                                                                                                                                                                                                                                                      |





To validate your own outputs against the schema you may use:

```bash
$ xmllint --schema opencost.xsd myfile.xml
```
