## General questions about the openCost project

1. **How can I contribute to the discussion?**

As we want to involve the community in our work as early as possible, we have decided to publish our project results successively in this GitHub repository and regularly obtain feedback. We therefore invite all interested parties to participate in the development of the metadata schema and look forward to a constructive discussion. You can open an GitHub issue at any time and contribute to the discussion with questions, comments or make suggestions for improving our scheme. You are also welcome to leave a comment or remark under other issues and thus participate in the discussion.

Alternatively, you can also send us feedback by e-mail or via our mailing list. We will then convert this into GitHub issues for you. We also regularly organize online discussions via Zoom to present changes or innovations to the schema to the community and then put them up for discussion. We will inform you about the dates via our website and the openCost mailing list (ur-ub-opencost.info@listserv.dfn.de).

2. **What are the requirements for implementing openCost in my institution?**

-> publication cost reporting in own internal format  
-> technically: OAI server & set definitions for automatic provision  
There must be an institution-specific system in which the publication costs are documented. This can be a repository or a library system, for example. Such an institution's own cost reporting system can be oriented on the concepts of openCost, but operates independently as an internal format. A technical format conversion would then take place between the internal format and the openCost exchange format. The second precondition for the automated exchange of cost data is the availability of an OAI server (with provisioning function, while harvesting is not necessary).  

3. **How does openCost relate to other formats?**

The openCost format is designed in a way that, in general, it can be used independently of other formats. As an exchange format for cost data that relies on the use of identifiers such as the DOI and tries to work as far as possible without bibliographic data, the openCost format is intended to be minimally redundant, so that it could also be easily integrated into other formats.  

See issue [#14](https://github.com/opencost-de/opencost/issues/14).   

## General questions about the openCost metadata schema

4. **Is it intended to additionally generate a JSON representation of the data?**

The community repeatedly asked whether the openCost schema could also be displayed in JSON format as an alternative. Previously, the use of XML attributes in the definition of the original openCost proposal stood in the way of this request, as attributes cannot be clearly mapped to JSON structures. The openCost schema has now been remodeled in an attribute-free version. Instead of XML attributes, type/value element combinations are used now. After weighing up all the pros and cons, the project team deliberately opted for this version to enable simple translation into other formats. 

See issue [#41](https://github.com/opencost-de/opencost/issues/41).  

5. **How should URLs be specified in the metadata schema (e.g. DOI)?**

For all urls given in the metadata schema the use of the https:// protocol prefix is necessary.  

See issue [#13](https://github.com/opencost-de/opencost/issues/13).  

6. **Is there a standard by which the values of currencies are defined in the openCost schema?**

For consistency and clear identification, currencies must be represented according to ISO 4217 (3-letter currency code, e.g. EUR, USD, etc.).

See issue [#30](https://github.com/opencost-de/opencost/issues/30).  

7. **Does the openCost scheme currently cover all costs of a scientific publication in terms of the total cost of publishing?**

openCost is designed as an exchange format, which is why data is recorded as sparingly as possible and as extensively as necessary. Therefore, in terms of the total cost of publishing currently not all costs are covered (such as staff, premises, hardware, software, etc.).  

See issue [#25](https://github.com/opencost-de/opencost/issues/25).  

## Schema for individual articles (`opencost:publication`)  

8. **How to deal with collective invoice for framework agreement with OA publishers?**

As long as the individual articles have a specific amount, this is not problematic, since an invoice number can be specified multiple times.

See issue [#38](https://github.com/opencost-de/opencost/issues/38).
   
9. **Can the `amount_invoice` be indicated in net and in gross; (possibly with reference to the corresponding amount of VAT)?**

All prices are net prices, the vat can be added as `type="vat"`:
   ```xml
     <opencost:amounts_paid>
        <opencost:amount_paid currency="EUR" type="gold-oa">1500.00</opencost:amount_paid>
        <opencost:amount_paid currency="EUR" type="vat">14.25</opencost:amount_paid>
      </opencost:amounts_paid>
   ```
See issue [#7](https://github.com/opencost-de/opencost/issues/7).  

10. **Is it possible to display zero or negative values for the `amounts_paid` in the schema?**

Yes, negative or zero values, e.g. for reimbursements, vouchers or Diamond OA models, can be specified for the `amount_paid` element (see documentation). Just set the price to 0 or a negative value, the costtype would be `gold-oa`:
   ```xml
     <opencost:amounts_paid>
        <opencost:amount_paid currency="EUR" type="gold-oa">0</opencost:amount_paid>
        <opencost:amount_paid currency="EUR" type="vat">0</opencost:amount_paid>
      </opencost:amounts_paid>
   ```  
See issue [#35](https://github.com/opencost-de/opencost/issues/35).  
  
11. **How do we address transformative agreements or memberships?**

By stating `part_of_contract` in the metadata of the publication concretely concerned you can link your publication to the specific agreement. `part_of_contract` then contains a mandatory primary identifier referring to the global contract, currently represented by an ESAC-ID. ESAC is an existing registry for transformative agreements. Additionally, it is possible to include `invoice_id` at this point to reference a particular invoice that occurred under this contract and includes a specific contract period. For detailed information please read the metadata documentation for contracts: https://github.com/opencost-de/opencost/tree/main/doc.
   
See issue [#11](https://github.com/opencost-de/opencost/issues/11).
