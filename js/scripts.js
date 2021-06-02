// Google sheets script
function connectToMongDB() {
    var sh1 = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("responses")
    var rng = sh1.getDataRange().getValues();
    for (var i = 1; i < rng.length; i++) {
        var discrod_name = rng[i][3].split("#");
        var formData = {
            'name': rng[i][1],
            'email': rng[i][2],
            'discord_name': discrod_name[0],
            'discord_tag': discrod_name[1],
            'codes_used': "",
            'workshops_attended': 0
        }
        var params = {
            'method': 'post',
            'payload': formData
        }
        var getId = UrlFetchApp.fetch("<URL-HERE>", params);

    }
}

// Realm Mongodb script
exports = async function(payload) {
 const mongodb = context.services.get("mongodb-atlas");
 const eventsdb = mongodb.db("Hack^2");
 const eventscoll = eventsdb.collection("users");

 x =  await eventscoll.findOne({"email" : payload.query.email, "discord_tag" : payload.query.discord_tag})
 try{
   return x.email
 }
 catch(err){
   const result= await eventscoll.insertOne(payload.query);
    var id = result.insertedId.toString();
   if(result) {
   return JSON.stringify(id,false,false);
   }
 }

 return { text: `Error saving` };
}
