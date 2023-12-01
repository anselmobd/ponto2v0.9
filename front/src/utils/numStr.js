export const ptBrCurrencyFormat = Intl.NumberFormat(
  'pt-BR', {
    style: 'decimal',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
    roundingMode: "halfEven",
  }
)
  
class NumberParser {
  constructor(locale) {
    const format = new Intl.NumberFormat(locale);
    const parts = format.formatToParts(12345.6);
    const numerals = Array.from({ length: 10 }).map((_, i) => format.format(i));
    const index = new Map(numerals.map((d, i) => [d, i]));
    this._group = new RegExp(`[${parts.find(d => d.type === "group").value}]`, "g");
    this._decimal = new RegExp(`[${parts.find(d => d.type === "decimal").value}]`);
    this._numeral = new RegExp(`[${numerals.join("")}]`, "g");
    this._index = d => index.get(d);
  }
  parse(str) {
    console.log('str', str, typeof str);
    return (str = str.trim()
    .replace(this._group, "")
    .replace(this._decimal, ".")
    .replace(this._numeral, this._index)) ? +str : NaN;
  }
}

export const ptBrNumberParser = new NumberParser('pt-BR');
