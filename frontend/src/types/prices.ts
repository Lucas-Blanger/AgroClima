export interface DailyPriceQuote {
  product_id: number;
  product_name: string;
  category: string;
  unit: string;
  price: string | number;
  date: string;
  source: string | null;
  variation: number | string | null;
}
