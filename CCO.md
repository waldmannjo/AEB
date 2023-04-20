# About Carrier Connect

Thank you for your interest in our Carrier Connect API. We would like to make it as easy as possible for you to get started using Carrier Connect. Please feel free to contact us if you miss information or if you find a way to make it even easier.

Let's start with the business object model of Carrier Connect. The main business object is the **shipment** which contains **packages** and usually has **items**. 

The shipment has a reference and contains, among other things, information about the shipper, recipient, shipping date, terms of delivery, carrier, and service.

# Basic concepts
## Steering workflow, data preparation, and printing

In addition to the business data like shipments, packages, and items, more information is needed to steer the workflow, prepare the correct data, print it at the right time in the right way, and finally know when everything is done.

In most API calls, there are basically two kinds of _parameter sets_' to provide the necessary information:

### CreationParms

See [here](doc:data-validation-and-error-handling-1)  for a detailed explanation.

```json
"creationParms": {
    "creationMode": "string"
  },
```
```xml
<creationParms>
      <creationMode>?</creationMode>
 </creationParms>
```



### ProcessParms

Explantions for [processMode](doc:synchron-or-asynchron) , [prepare and output scopes](doc:prepare-and-output-scope) and [documentOutputMode](doc:printing-documents) are available in the "Basic concepts" section.

```json
"processParms": {
    "processMode": {
      "mode": "string"
    },
    "documentPrepareScope": {
      "scope": "string"
    },
    "workstationId": "string",
    "documentOutputScope": {
      "scope": "string"
    },
    "documentOutputMode": {
      "mode": "string"
    },
    "doCompletion": true
  },
```

```xml
<processParms>
     <processMode>
          <mode>?</mode>
     </processMode>
     <documentPrepareScope>
          <scope>?</scope>
     </documentPrepareScope>
     <workstationId>?</workstationId>
     <documentOutputScope>
         <scope>?</scope>
     </documentOutputScope>
     <documentOutputMode>
         <mode>?</mode>
     </documentOutputMode>
     <doCompletion>?</doCompletion>
</processParms>
```



### Workstation ID

Most of the requests require a _Workstation ID_.  
Workstations are part of the master data which needs to be set up in Carrier Connect. A workstation has assigned printers (usually for label printing and standard (general) printing. Based on the assigned printers, the output format (PDF, ZPLII, etc.) is determined.  
Without a workstation, Carrier Connect cannot prepare or print any data or documents.

### doCompletion

This is a simple true/false parameter indicating whether a <<glossary:shipping order>> has been completed or whether further operations like adding more packages, items, etc. have been planned for it.  
Once a shipment has been completed, it can no longer be changed apart from canceling it.  
Only completed shipments can be assigned to pickups. If a carrier is set up with automatic pickup disposal, all completed shipments will be automatically assigned to a pickup.

## Data validation and error handling

### Creation Modes

Any data sent to Carrier Connect must be validated:  
Is the zip code correct? Does the carrier allow to ship packages with these dimensions? Is all required data available? These and many more checks are performed every time new shipments, packages, items, etc. are to be created.

Carrier Connect allows you to choose between various _creation modes_ which determine the behavior for data creation and error handling.

#### Creation mode "ALWAYS"

The shipment/packages is/are created even if validation fails and validation warnings are returned. Those warnings can either be corrected manually using the Carrier Connect UI or the shipment has to be canceled via the _cancelShipment_ API call and retransmitted with a _createShipment_ call. The cancellation step is necessary because a direct retransmission of existing shipments and packages is not allowed.  
In addition, it is possible to configure Carrier Connect to respond with an "error label" which contains the error and/or warnings. This helps also to at least have "something" to put on the package if the real carrier label could not be created.

```json
... 
"creationParms": {
    "creationMode": "ALWAYS"
  },
...
```



#### Creation mode "VALIDATION_OK"

The shipments, packages, or items are only created if the shipment could be successfully validated. Otherwise, validation warnings will be returned in the response. A direct retransmission, after reviewing the data, is possible since no data has been created by the initial call.

```json
... 
"creationParms": {
    "creationMode": "VALIDATION_OK"
  },
...
```



### Error handling

If errors or warnings occur, the API response will always have header information indicating the type (error, retryable error, and/or warnings) and contains the related messages.

```json
{
  "hasErrors": true,
  "hasOnlyRetryableErrors": false,
  "hasWarnings": false,
  "messages": [
    {
      "messageType": "ERROR",
      "messageIdentCode": "PICKUP_NOT_FOUND_ERROR",
      "messageTexts": [
        {
          "languageISOCode": "en",
          "text": "Unable to find pickup for Pickup Pickup no. ..."
        }
      ],
      "indentationLevel": 0
    }
  ]
}
```



**hasErrors**  
An error is returned if the operation couldn't be performed because of a basic issue (non-unique transactionIds or if data cannot be found in the system, as in the example above).  
**hasOnlyRetryableErrors**  
If all errors are retryable errors, e.g. some data was locked, this is indicated.  
**hasWarnings**

Note: At the moment, the _indentationLevel_ is not used. It is always "0".


## Understanding data and document generation

### Preparation and output scopes

A distinct feature of Carrier Connect is the possibilty to separate the creation (generation) of documents completely from printing them.  
This is done by setting the right _scope_ for preparation and also for the desired output.

Of course, documents can be generated and requested for printing at the same time. This is easy and no problem!  
However, it is also possible to split up the process and just generate documents and request them for printing later.  
Sometimes it is also necessary to print or re-print documents for a specific package, rather than all documents for the complete shipment.

**Available scopes**  
The following scopes can be used to determine what to "prepare" and what to "output":  
**NONE**  
No preparation and no output will happen. This is the default when scope is left empty.  
**ALL**  
All documents including the already processed ones are considered.  
**REMAINING**  
Only the remaining, not yet processed documents are considered.  
**REQUEST**  
Only documents for the packages included in the specific API call are considered.  
**SHIPMENTONLY**  
No package documents are processed. The shipment (header) is prepared. All possible calculations like routing data are calculated. This leads to improved performance when package documents are prepared.

**Example:**  
Many of our customers use the following API calls to make use of this distinct feature:

_1) createShipment_ (in order to create a shipment)  
documentPrepareScope = SHIPMENTONLY  
documentOutputScope = NONE  
The shipment (header) data is validated and all necessary data is calculated e.g. routing date, tracking numbers on shipment level, etc. No output is generated.

```json
"processParms": {
   ...
    "documentPrepareScope": {
      "scope": "SHIPMENTONLY"
    },
    "documentOutputScope": {
      "scope": "NONE"
    },
    "documentOutputMode": {
      "mode": "NONE"
    },
    "doCompletion": false
  },
```
```xml
<processParms>
  ...
     <documentPrepareScope>
         <scope>SHIPMENTONLY</scope>
     </documentPrepareScope>
     <documentOutputScope>
         <scope>NONE</scope>
     </documentOutputScope>
     <documentOutputMode>
         <mode>NONE</mode>
     </documentOutputMode>
  	 <doCompletion>false</doCompletion>
</processParms>
```



_2) processShipment_ (in order to add one or more packages)  
documentPrepareScope = REQUEST  
documentOutputScope = REQUEST  
All data and documents related to the packages created in this specific request are calculated and prepared. The generated documents will be returned in the response to the API call.

```json
"processParms": {
   ...
    "documentPrepareScope": {
      "scope": "REQUEST"
    },
    "documentOutputScope": {
      "scope": "REQUEST"
    },
    "documentOutputMode": {
      "mode": "RETURN"
    },
    "doCompletion": false
  },
```
```xml
<processParms>
  ...
     <documentPrepareScope>
         <scope>REQUEST</scope>
     </documentPrepareScope>
     <documentOutputScope>
         <scope>REQUEST</scope>
     </documentOutputScope>
     <documentOutputMode>
         <mode>RETURN</mode>
     </documentOutputMode>
  	 <doCompletion>false</doCompletion>
</processParms>
```



_This example provides an ideal API workflow to optimize performance and data processing for label printing on the package level!_

## Synchronous or asynchronous

### Processing mode

API calls can be performed synchronously or asynchronously.

These options are provided to match the shipping context and the technical capabilities of the calling system.  
_Synchronous_ communication responds with more distinct results. No additional lookup to verify the final result of an operation is needed. On the other hand, it closely links the calling system with Carrier Connect and sometimes it might be preferable to avoid this.  
In the _asynchronous_ communication mode, Carrier Connect checks whether it is generally possible to perform an operation (e.g. check transactionId for uniqueness) and accepts the task if no issues are detected. Only then, more sophisticated validations are performed. The calling system only learns about possible warnings by frequently synchronizing with Carrier Connect using the sync calls of the API.

**Process mode "BASIC"**  
Triggers asynchronous communication. Default mode if nothing else is provided.  
The operation is processed in an asynchronous job after performing some basic checks.

```json
"processParms": {
    "processMode": {
      "mode": "BASIC"
    },
...
```
```xml
<processParms>
     <processMode>
         <mode>BASIC</mode>
     </processMode>
     ...
</processParms>
```



**Process mode "EXTENDED"**  
Triggers synchronous communication.  
The operation is executed directly within the API request transaction and no response is returned until the process is finished.

```json
"processParms": {
    "processMode": {
      "mode": "EXTENDED"
    },
...
```
```xml
<processParms>
     <processMode>
         <mode>EXTENDED</mode>
     </processMode>
     ...
</processParms>
```

## Printing documents

### Output modes

Creating documents like labels and loading list is an essential part of Carrier Connect.  
Ideally, Carrier Connect simply creates all necessary documents and returns them in the response of the API call. If assynchronous communication is used, the documents can be retrieved at any time after creation using e.g. the sync API calls.

The way documents are printed can be determined by the _document output mode_:

**Output mode RETURN**  
This is the preferred mode when working synchronously.  
All requested documents will be returned in the response to the API call.

```xml
...
<documentOutputScope>
  <scope>RETURN</scope>
</documentOutputScope>
...
```
```json
{ 
  ...
   "documentOutputScope": {
      "scope": "RETURN"
    },
  ...
}
```



**Output mode NONE**  
No output will be generated. This is independent from the document generation itself. This parameter simply means that there will be no outpout of documents.  
In more complex shipping scenarios, it can be useful to generate documents ahead of time and to request them for printing only at a later stage.

```xml
...
<documentOutputScope>
  <scope>NONE</scope>
</documentOutputScope>
...
```
```json
{ 
  ...
   "documentOutputScope": {
      "scope": "NONE"
    },
  ...
}
```



**Output mode PRINT**  
This is a special mode if the requesting ERP system has no own printing capabilities and works only in connection with an _AEB printing agent_.  
Using this mode will result in print jobs assigned to the _workstation ID_ used in the API call. The _AEB print agent_ must run on the client system responsible for printing and constantly polls for print jobs using a specific _workstation ID_.  
Note: This should not be the first choice for printing since printing performance is not as good as when using the _RETURN mode_ and more information about the printing infrastructure e.g. the specific printers (not just the type of printers) must be provided in Carrier Connect.

```xml
...
<documentOutputScope>
  <scope>PRINT</scope>
</documentOutputScope>
...
```
```json
{ 
  ...
   "documentOutputScope": {
      "scope": "PRINT"
    },
  ...
}
```

## Referencing data

**Referencing shipments**  
When creating a shipment, the calling system can provide a _transactionId_ and a _referenceNumber1_ which can be used to identify the shipment in subsequent API calls.  
Whenever a shipment is successfully created, Carrier Connect assigns a _shipmentNumber_ to it. This number can be used to identfify the shipment as well.

The _transactionId_ (the calling system has to ensure this) and the _shipmentNumber_ are always unique within the customer's client setup in Carrier Connect.  
Any none-unique _transactionId_ will be rejected and result in an error.

The _referenceNumber1_ does not have to be unique which makes it a weak reference and it is not recommended to use it as the sole reference.

```json
"shipmentReference": {
    "transactionId": "string",
    "referenceNumber1": "string",
    "shipmentNumber": "string"
  }
```



**Referencing packages**  
Referencing packages is based on the same principles as described above.  
Packages can be identified by the _packageTransactionId_ which must be unique within the shipment and/or the package's _referenceNumber1_.  
To provide the correct context, the shipment containing the package must be referenced as well.

```json
"packageReference": {
    "shipmentReference": {
      "transactionId": "string",
      "referenceNumber1": "string",
      "shipmentNumber": "string"
    },
    "packageTransactionId": "string",
    "referenceNumber1": "string"
}
```



**Referencing items**  
Items can be identified by the _itemtransactionId_ which must be unique within the shipment and/or the item's _referenceNumber1_. These fields are contained in the _shipmentItemReference_ structure which also holds a _shipmentReference_ to identify the shipment.  
The _quantityValue_ can be ignored. It is only applied when items are packed into different packages.

```json
"shipmentItemReference": {
    "shipmentReference": {
      "transactionId": "string",
      "referenceNumber1": "string",
      "shipmentNumber": "string"
    },
    "itemTransactionId": "string",
    "referenceNumber1": "string",
    "quantityValue": 0
}
```