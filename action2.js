function transform(data) {
  var result;

  if(data.tSoil_C_hummock < 0.1)
    result = {
        "agent": "OpenWhisk action",
        "irrigation": "on"
    };
  else
    result = {
        "agent": "OpenWhisk action",
        "irrigation": "off"
    };

  return JSON.stringify(result);
}

function main(params) {
  console.log("DEBUG: Received message as input: " + JSON.stringify(params));
  return { "value": transform(params)};
}