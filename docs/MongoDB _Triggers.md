# MongoDB Triggers - Mapping on the Database Side 
Occasionally, you might have an operation that occurs on the database side of the sensor network, where it is easier, more efficient, or better defined to have the operation occur when a new record is created. For example, in our sensor network system, we have one type of sensor which unfortunately does not have a persistent ID. Because of this, the ID is regularly checked and mapped to a persistent label. Rather than continuously checking the database for the mapping before insert, this is easier to conduct on the database-side itself using triggers. This documentation walks through that process. 

## Setup 
We are using the MongoDB Atlas GUI to create our triggers. However, for local mongo, there is potentially ways to do this using change streams (though our program has not yet looked into this). 

## Create the Trigger
When you open the cluster, under the "Services" Menu, you should see a "Triggers" option. Click on that and create a new Trigger. 

## Trigger Details

- Trigger Type: **Database**
- Watch Against: **Collection**
- Cluster Name: **your_cluster_name** (you should have a dropdown to choose)
- Database Name: **your_database_name** (you should have a dropdown to choose)
- Collection Name: **your_collection_name** (you should have a dropdown to choose)
- Operation Type: **Insert Document**
- Leave Full Document and Document Pre-Image options **unchecked** 

## Trigger Configurations
Can leave defaults checked 

## Event Type
- Select an Event Type: **Function** 

## Function 


    exports = async function(changeEvent) {
    // A Database Trigger will always call a function with a changeEvent.
    // Documentation on ChangeEvents: https://docs.mongodb.com/manual/reference/change-events/

    // This sample function will listen for events and replicate them to a collection in a different Database
    //console.log(JSON.stringify(changeEvent))

    // Access the _id of the changed document:
    const docId = changeEvent.documentKey._id;

    // Get the MongoDB service you want to use (see "Linked Data Sources" tab)
    // Note: In Atlas Triggers, the service name is defaulted to the cluster name.
    const serviceName = "HarborCenter";
    const database = "SCARECRO";
    const match_collection_name = "weather_rack_instances";
    const match_collection = context.services.get(serviceName).db(database).collection(match_collection_name);
    const main_collection = context.services.get(serviceName).db(database).collection(changeEvent.ns.coll);

    //Get the matching label 
    const query = { "mapped_id": changeEvent.fullDocument.id };
    //const generatedObjectId = BSON.ObjectId(docId)
    //console.log("Object ID", generatedObjectId)
    const update_query = {"_id": docId};
    //const update_query = {"id": 32};


    // Get the "FullDocument" present in the Insert/Replace/Update ChangeEvents
    try {
        // If this is a "delete" event, delete the document in the other collection
        if (changeEvent.operationType === "insert") {
        //console.log("inside the insert operation");
        mapping_doc = await match_collection.findOne(query);
        //console.log("Mapping ID: ", mapping_doc.mapping_id);
        return await main_collection.updateOne(update_query, {$set: {"label": mapping_doc.instance_id}});
        //return await main_collection.updateOne(update_query, updateFields);
        }
    } catch(err) {
        console.log("error performing mongodb write: ", err.message);
    }
    };


## Explaining the Function 
We have documents coming into the database **weather_rack** with a field named **id**. We want the **id** field to match the **mapped_id** field in the database **weather_rack_instances**. When the matching document is found, we will set the **label** field on the **weather_rack** document to the **instance_id** field on the **weather_rack_instances** document. 

- match_collection_name: The name of the collection where we will match the field, in this case, **weather_rack_instances**
- query: the match operation. In this case, we want our **weather_rack id** field to match the **mapped_id field of weather_rack_instances**
- main_collection: the collection that the trigger executes on an insert, in this case **weather_rack**
- update_query: the document to update, in this case, the same document we inserted, matched with the mongo-document-specific **_id** field. 
- updateOne: When we match the query, we set the label of the **weather_rack** document to the **instance_id** of the **weather_rack_instances** document 


## Trigger Name
Give a descriptive name for your trigger. We used **Add_Label_Weather_Rack**

Then you can save your trigger. Make sure it is enabled if you want it to make changes to your data. 

## Final Thoughts
There is much more functionality for MongoDB Triggers and you can look into your different options and performance characteristics of each. There are limits on how many triggers you are allowed in MongoDB free tier. 

