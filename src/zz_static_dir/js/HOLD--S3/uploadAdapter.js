// importing these using CDN
// import AWS from 'aws-sdk';
// import imageCompression from 'browser-image-compression';

class S3UploadAdapter {
  constructor(loader, accountID) {
    // The file loader instance to use during the upload.
    this.loader = loader;
    // The account ID used to construct the S3 prefix.
    this.accountID = accountID;
  }

    async upload() {
      if (!this.loader.file || typeof this.loader.file !== 'object') {
        throw new Error('Invalid file object');
      }
      
      const awsAccessKey = 'YDI52ZS4AW2NDEABYWBS'
      const awsSecretKey = '0vGYAUN5uKmga8d4kjXGsMNoCeyPEi3NW6nf0IS8YeE'
      const awsRegion = 'fra1'
      const awsBucket = 'sodavault-stage'
        
      const data = await this._processImage(this.loader.file);
      const { original, resized50, resized25 } = data;

      // Initialize the S3 client.
      const s3 = new AWS.S3({
        accessKeyId: awsAccessKey,
        secretAccessKey: awsSecretKey,
        region: awsRegion,
      });

      // Upload the original image.
      const originalKey = `${this.accountID}/ckeditor/${original.name}`;
      await s3.upload({
        Bucket: awsBucket,
        Key: originalKey,
        Body: original.data,
        ACL: 'public-read',
        ContentType: original.type // Add the content type
      }).promise();

      // Upload the 50% resized image.
      const resized50Key = `${this.accountID}/ckeditor/${resized50.name}`;
      await s3.upload({
        Bucket: awsBucket,
        Key: resized50Key,
        Body: resized50.data,
        ACL: 'public-read',
        ContentType: 'image/jpeg' // Use a fixed content type for resized images
      }).promise();

      // Upload the 25% resized image.
      const resized25Key = `${this.accountID}/ckeditor/${resized25.name}`;
      await s3.upload({
        Bucket: awsBucket,
        Key: resized25Key,
        Body: resized25.data,
        ACL: 'public-read',
        ContentType: 'image/jpeg' // Use a fixed content type for resized images
      }).promise();

      // Return the uploaded URLs.
      return {
        default: `https://${awsBucket}.s3.amazonaws.com/${originalKey}`,
        sizes: {
          '50%': `https://${awsBucket}.s3.amazonaws.com/${resized50Key}`,
          '25%': `https://${awsBucket}.s3.amazonaws.com/${resized25Key}`,
        },
      };
    }

    async _processImage(file) {
      const original = {
        name: file.name,
        data: file,
      };

      const compressed = await this._compressImage(file);

      const resized50 = {
        name: `${compressed.name}_50p.jpg`,
        data: await this._resizeImage(compressed.file, 0.5),
      };

      const resized25 = {
        name: `${compressed.name}_25p.jpg`,
        data: await this._resizeImage(compressed.file, 0.25),
      };

      return {
        original,
        resized50,
        resized25,
      };
    }

async _compressImage(file) {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = () => {
      const img = new Image();
      img.onload = () => {
        const elem = document.createElement('canvas');
        const width = img.naturalWidth;
        const height = img.naturalHeight;
        const max = 1000;
        let w = width;
        let h = height;
        if (width > height && width > max) {
          w = max;
          h = Math.round((max * height) / width);
        } else if (height > max) {
          h = max;
          w = Math.round((max * width) / height);
        }
        elem.width = w;
        elem.height = h;
        const ctx = elem.getContext('2d');
        ctx.drawImage(img, 0, 0, w, h);
        ctx.canvas.toBlob(
          (blob) => {
            const compressedFile = new File([blob], `${file.name}_compressed.jpg`, {
              type: 'image/jpeg',
              lastModified: Date.now(),
            });
            resolve({ file: compressedFile, name: compressedFile.name });
          },
          'image/jpeg',
          1
        );
      };
      img.src = reader.result;
    };
    reader.readAsDataURL(file instanceof Blob ? file : file.file);
  });
};
}



function S3UploadAdapterPlugin(editor) {
editor.plugins.get('FileRepository').createUploadAdapter = (loader) => {
  const accountID = 'YOUR_ACCOUNT_ID'; // Replace with your account ID.
  return new S3UploadAdapter(loader, accountID);
};
}

window.MyCustomUploadAdapterPlugin = S3UploadAdapterPlugin;
