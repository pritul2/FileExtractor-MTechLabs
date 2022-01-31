const fs = require('fs');
const dir = '../../static/Zip_Extracted';

fs.readdir(dir, (err, files) => {
  console.log(files.length);
});