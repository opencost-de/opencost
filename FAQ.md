## General questions

1. **How can I contribute to the discussion?**

As we want to involve the community in our work as early as possible, we have decided to publish our project results successively in this GitHub repository and regularly obtain feedback. We therefore invite all interested parties to participate in the development of the metadata schema and look forward to a constructive discussion. You can open an GitHub issue at any time and contribute to the discussion with questions, comments or make suggestions for improving our scheme. You are also welcome to leave a comment or remark under other issues and thus participate in the discussion.

Alternatively, you can also send us feedback by e-mail or via our mailing list. We will then convert this into GitHub issues for you. We also regularly organize online discussions via Zoom to present changes or innovations to the schema to the community and then put them up for discussion. We will inform you about the dates via our website and the openCost mailing list (opencost.info@mailman. uni-regensburg.de).

2. **Is it intended to additionally generate a JSON representation of the data?**

We are first developing the XML schema. Background is the OAI interface and the fact that the project partners use repositories, which in connection with OAI-PMH have
mostly established xml as exchange format. On the other hand, we do not want to complicate the discussion by putting two schemas up for disposition. In a further step, we want to convert the XML into a JSON format.  
See issue [#41](https://github.com/opencost-de/opencost/issues/41).  

3. **What are the requirements for implementing openCost in my institution?**

-> publication cost reporting in own internal format  
-> technically: OAI server & set definitions for automatic provision  
There must be an institution-specific system in which the publication costs are documented. This can be a repository or a library system, for example. Such an institution's own cost reporting system can be oriented on the concepts of openCost, but operates independently as an internal format. A technical format conversion would then take place between the internal format and the openCost exchange format. The second precondition for the automated exchange of cost data is the availability of an OAI server (with provisioning function, while harvesting is not necessary).  

4. **How should URLs be specified in the metadata schema (e.g. DOI)?**

For all urls given in the metadata schema the use of the https:// protocol prefix is necessary.  
See issue [#13](https://github.com/opencost-de/opencost/issues/13).  

5. **How does openCost relate to other formats?**

The openCost format is designed in a way that, in general, it can be used independently of other formats. As an exchange format for cost data that relies on the use of identifiers such as the DOI and tries to work as far as possible without bibliographic data, the openCost format is intended to be minimally redundant, so that it could also be easily integrated into other formats.  
See issue [#14](https://github.com/opencost-de/opencost/issues/14) 

## Schema for individual articles

1. **How to deal with collective invoice for framework agreement with OA publishers?**

As long as the individual articles have a specific amount, this is not problematic, since an invoice number can be specified multiple times.

See issue [#38](https://github.com/opencost-de/opencost/issues/38).
   
2. **Can the `amount_invoice` be indicated in net and in gross; (possibly with reference to the corresponding amount of VAT)?**

All prices are net prices, the vat can be added as `type="vat"`:
   ```xml
     <opencost:amounts_paid>
        <opencost:amount_paid currency="EUR" type="apc">1500.00</opencost:amount_paid>
        <opencost:amount_paid currency="EUR" type="vat">14.25</opencost:amount_paid>
      </opencost:amounts_paid>
   ```
See issue [#7](https://github.com/opencost-de/opencost/issues/7).
   
3. **How do we address transformative agreements or memberships?**

By stating `part_of_contract` in the metadata of the publication concretely concerned you can link your publication to the specific agreement. `part_of_contract` then contains a mandatory primary identifier referring to the global contract, currently represented by an ESAC-ID. ESAC is an existing registry for transformative agreements. Additionally, it is possible to include `invoice_id` at this point to reference a particular invoice that occurred under this contract and includes a specific contract period. For detailed information please read the metadata documentation for contracts: https://github.com/opencost-de/opencost/tree/main/doc.
   
See issue [#11](https://github.com/opencost-de/opencost/issues/11).
