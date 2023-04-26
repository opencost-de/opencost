1. **How to deal with collective invoice for framework agreement with OA publishers?**

   As long as the individual articles have a specific amount, this is not problematic, since an invoice number can be specified multiple times.
   [#38](https://github.com/opencost-de/opencost/issues/38)
   
1. **Can the `amount_invoice` be indicated in net and in gross; (possibly with reference to the corresponding amount of VAT)?**

   All prices are net prices, the vat can be added as `type="vat"`:
   ```xml
     <opencost:amounts_paid>
        <opencost:amount_paid currency="EUR" type="apc">1500.00</opencost:amount_paid>
        <opencost:amount_paid currency="EUR" type="vat">14.25</opencost:amount_paid>
      </opencost:amounts_paid>
   ```
   [#7](https://github.com/opencost-de/opencost/issues/7)
   
1. **How do we address transformative agreements or memberships?**

   The initially proposed format does not yet handle transformative agreements like DEAL, but assumes article based fees only. This is a restriction made to enable as early as    possible involvement with the community. In the future this information will be indicated in the field `part_of_contract`.
   
   [#11](https://github.com/opencost-de/opencost/issues/11)

1. **Is it intended to additionally generate a JSON representation of the data?**

   We are first developing the XML schema. Background is the OAI interface and the fact that the project partners use repositories, which in connection with OAI-PMH have
   mostly established xml as exchange format. On the other hand, we do not want to complicate the discussion by putting two schemas up for disposition. In a further step, we
   want to convert the XML into a JSON format.
   
   [#41](https://github.com/opencost-de/opencost/issues/41)