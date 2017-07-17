
# Marina

# Boats <!-- Boat Start -->

## Create a boat
```
POST /boats
```

Name        | Type        | Description
------------|:-----------:|--------------:
name        | String      | Name of the vessel
type        | String      | Type of vessel
length      | Integer     | Length of the vessel
at_sea      | Bool        | True if vessel at Sea

## List all boats
```
GET /boats
```

## List a single boat
```
GET /boats/:id
```

## Mark a boat as at sea
```
PUT /boats/:id/sea
```

## Modify a boat
```
PATCH /boats/:id
```

Name              | Type    | Description
------------------|:-------:|--------------:
Name (optional)   | String  | Updated name of the vessel
Type (optional)   | String  | Updated type of the vessel
Length (optional) | Integer | Updated length of the vessel
at_sea (optional) | Bool    | Updated state of the vessel


## Replace a boat
```
PUT /boats/:id
```

Name              | Type    | Description
------------------|:-------:|--------------:
Name (optional)   | String  | Updated name of the vessel
Type (optional)   | String  | Updated type of the vessel
Length (optional) | Integer | Updated length of the vessel
at_sea (optional) | Bool    | Updated state of the vessel

## Delete a boat
```
DELETE /boats/:id
```

<!-- Boat End -->


# Slips  <!-- Slip Start -->

## Create a slip

```
POST /slips
```

Name        | Type        | Description
------------|:-----------:|--------------:
Number      | Integer     | Slip designation Number

## List all slips
```
GET /slips
```

## List a single slip
```
GET /slips/:id
```

## List the boat docked at a slip
```
GET /slips/:id/dock
```

## Mark a boat as docked a boat at a slip
```
PUT /slips/:slipID/dock/:boatID
```

## Mark a boat as undocked from a slip
```
DELETE /slips/:slipID/dock/:boatID
```

## Modify a slip
```
PATH /slips/:id
```

Name                    | Type        | Description
----------------------- |:-----------:|--------------:
Number (optional)       | Integer     | Updated slip designation number
Arrival Date (optional) | String      | Updated Boat arrivial date
Boat Docked (optional)  | Boat ID     | Updated current Boat ID of docked boat.

## Replace a slip
```
PUT /slips/:id
```

Name                    | Type        | Description
----------------------- |:-----------:|--------------:
Number (optional)       | Integer     | Updated slip designation number
Arrival Date (optional) | String      | Updated Boat arrivial date
Boat Docked (optional)  | Boat ID     | Updated current Boat ID of docked boat.

## Delete a slip
```
DELETE /slips/:id
```

<!-- Slip End -->
