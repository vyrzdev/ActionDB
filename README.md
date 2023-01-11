# ActionDB
### A Proof-Of-Concept ~database? storing state in a github repository.


## Commands:
C: Create Collection <- Done

P: Push to collection <- Done

R: Remove Collection

U: Update entity

D: Delete entity

-----------------
Example usage: Alternative Frontend for Online Store;
```
Github action on push to journal.txt
    - Builds DB from journal
    - Generates new API state
    - Pushes new pricing to sale-provider (etsy/shopify, where transaction occurs)
    - (^^^ or to internal provider on cloudflare workers)

Static Web Client
    - Browse Products, build a cart.
    - On checkout, redirect to sales-provider with cart details.
    
Admin Client
    - Can be anything, discord bot, manual user, static web with github auth.
    - Takes commands, can be abstracted away from
      ActionDB, generates journal commands from them
    - Pushes new journal commands.
```