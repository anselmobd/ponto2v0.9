export function floatRound(number, digits = 0) {
  var multiplicator = Math.pow(10, digits);
  return Math.fround(number * multiplicator) / multiplicator;
}
