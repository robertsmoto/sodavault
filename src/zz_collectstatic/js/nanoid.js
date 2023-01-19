function generateNanoid(size) {
  size = size || 21;
  var alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var allowedChars = alphabet.split('');
  var nanoid = '';
  while (nanoid.length < size) {
    var index = Math.floor(Math.random() * allowedChars.length);
    nanoid += allowedChars[index];
  }
  return nanoid;
};
