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
