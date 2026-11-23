/**
 * Cloudflare Worker / Pages Function
 * Proxies stock price requests from Yahoo Finance with CORS enabled.
 * 
 * Can be deployed to Cloudflare Workers or used as a Pages Function.
 * Endpoint: /api/stock-prices or https://your-worker.workers.dev
 */

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Cache-Control": "public, max-age=60" // Cache edge response for 60s
};

export default {
  async fetch(request, env, ctx) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const symbolsParam = url.searchParams.get("symbols") || "MSTR,PLTR,HOOD,HIMS,NFLX,BABA,NOW,MARA,CZR,OSCR,SOFI";
    const symbols = symbolsParam.split(",").map(s => s.trim().toUpperCase()).filter(Boolean);

    const priceMap = {};
    const detailsMap = {};

    await Promise.all(
      symbols.map(async (sym) => {
        try {
          const res = await fetch(`https://query2.finance.yahoo.com/v8/finance/chart/${sym}?interval=1d&range=1d`, {
            headers: {
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
              "Accept": "application/json"
            }
          });
          if (res.ok) {
            const data = await res.json();
            const meta = data?.chart?.result?.[0]?.meta;
            if (meta?.regularMarketPrice != null) {
              const price = Math.round(Number(meta.regularMarketPrice) * 100) / 100;
              const prev = meta.chartPreviousClose || meta.previousClose || price;
              const prevClose = Math.round(Number(prev) * 100) / 100;
              const change = Math.round((price - prevClose) * 100) / 100;
              const changePct = prevClose > 0 ? Math.round((change / prevClose) * 10000) / 100 : 0;

              priceMap[sym] = price;
              detailsMap[sym] = {
                price,
                previousClose: prevClose,
                change,
                changePercent: changePct
              };
            }
          }
        } catch (err) {
          // Skip errored symbol
        }
      })
    );

    const payload = {
      updated_at: new Date().toISOString(),
      updated_timestamp: Math.floor(Date.now() / 1000),
      count: Object.keys(priceMap).length,
      prices: priceMap,
      details: detailsMap
    };

    return new Response(JSON.stringify(payload, null, 2), {
      headers: {
        ...CORS_HEADERS,
        "Content-Type": "application/json; charset=utf-8"
      }
    });
  }
};
