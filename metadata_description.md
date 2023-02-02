**Metadata fior costs of publication:**

Scholarly publications are very good described by standardized metadata.
Existing frameworks focus on bibliographic description, legal aspects
including access rights, and technical metadata like size of files etc.

Up to know - at least to our knowledge - there exists no metadataformat
for describing financial aspects of publications. But during the process
of transforming the scholarly publishing to Open Access, transparency is
necessary. Otherwise there exists the possibility of increasing costs.
In collaboration with a lot of stakeholder we developed a metadata
scheme for payment data. This includes payment for single articles,
transformative agreements but can easily be adopted to subscription
costs. We try to consider all costs related to publication (Total cost
of Publishing) including OA, non-OA costs as well as costs for
processing fees (like costs for bank transfer, credit cards etc.). With
this approach we try to get an overview over all payments to publishing
houses of an institution (so called information budget) and due to the
standardized format and machine readability to achieve a broader
understanding of payments trough out the world to publishers.

We introduce this metadatascheme, propose an xml-representation and are
open to discuss it. You can compare the scheme to your payment, ask
about any doubts, and are invited to upload further examples.

Let's start the discussion!

**Metadata scheme for publications:**


| **Fieldname** | **Description** | **Type** | **Multiple** | **Required** | **Value Required** | **Remarks** |
|---------|---------|---------|---------|---------|---------|---------|
| doi     | DOI to identify the publication | string  | No | Yes| No | Preferably the DOI mentioned on the publication (Version of Record). If no identifier exists, it has to be an empty field     |
| id      | identifier of the publication. This can be a doi, handle, urn, an isbn, pmid, pmc, arxiv, oai, localidentifier    | String  | Yes     | No      | No      |         |
| institution    | the institution, who pays for the publication. This should be given also as an open identifier preferably the ror-ID.ISNI, Ringold | String  | Yes     | Yes     | Yes     | Specified if PID, Name or anything else      |
| type|the type of the publication described by the COAR controlled vocabulary | String  |         | Yes     | Yes     | This field explains the type of the publication, how the reporting institutions categorize it. Maybe this will differ from the type mentioned by publisher, databases or elsewhere. |
| bibliographic_information| information about the publication. | String | | No/Yes | No | This field is mandatory if no identifier exists, otherwise it is optional. Structured as DC or (better) Datacite |
| oa_status_orig | status of the publication at the time of publication electronically | String  | | Yesi | Yes | Values: open, closed, hybrid |
| part_of_contract | if the publication is part of special contract | String  | | No | No | e.g. a transformative agreement, a membership, central invoicing, community publication models etc.
Maybe the ESAC registry ID |
| **For each payment one block**   |         |         |         |         |         |         |
| amount_invoice | price written on the invoice in the given currency | Number  | | No | No | float |
| invoice_number | number of the invoice  | String  | | No | No | |
| amount_paid | the actual amount paid by the institutions in the currency | Number  | | Yes | Yes | One entry for each payment, can be repeated, e.g. payment of APC and VAT |
| type    | what kind of payment | String  |         | Yes     | Yes     | e.g. colour charges, pagecharges, apc, bpc, cover charge, controlled vocabulary |
| date_paid | date of the payment | String  | | Yes | Yes | YYYY-MM-DD Recommended exact day. Minimal resolution year   |
| publisher     | name of the publisher mentioned at the invoice | String  |         | No      | No      | might not be the actual publisher, where the publication is published, e.g. service from an other publisher |

**Metadata schema for contracts**

| **Fieldname** | **Description** | **Type** | **Required** | **Value Required** | **Remarks** |
|---------|---------|---------|---------|---------|---------|
| id | id of contract |string | yes | yes | If exists, it should be the ESAC registry ID, otherwise it can be chosen by the institution |
| name     | Name of the contract | string | yes | yes | human readable |
| date_start | starting date of the contract | string | yes | yes | YYYY-MM-DD |
| date_end | ending date of the contract | string | yes | yes | YYYY-MM-DD |
| relevant_date_publication | information about the decision whether publication is included in the contract | string | yes | no | one of the following values: submitted, accepted or published |
| **Followed by one or more blocks about the payment**   |         |         |         |         |         |
| payment  | information about a payment |          |          |          | Element for each payment  |
| amount   | money paid in currency for each position on the invoice specified in currency and the type for which th amount was paid| Number   | Yes      | Yes      | Possible values:
publish, read, consortial, ...|
| period   | from … to …. | String   | no       | no       | Period for which the payment is valid, if this field not exists, the payment is for the whole duration of the contract  |



      
