import re
import time
import random
from playwright.sync_api import sync_playwright

# ---------------- Site detection ----------------
def detect_site(url):
    if "flipkart.com" in url:
        return "flipkart"
    if "amazon." in url:
        return "amazon"
    if "snapdeal.com" in url:
        return "snapdeal"
    return None

"""# ---------------- FLIPKART (Playwright — most reliable) ----------------
def scrape_flipkart(url):
    reviews = []
    product_name = "Flipkart Product"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768},
            locale="en-IN",
        )
        page = context.new_page()

        try:
            print(f"[Flipkart] Loading product page...")
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

            # Close login popup if present
            try:
                page.click("button:has-text('✕')", timeout=2000)
            except Exception:
                pass

            # Product name
            try:
                product_name = page.locator("span.B_NuCI, h1 span").first.text_content(timeout=3000) or product_name
                product_name = product_name.strip()[:120]
            except Exception:
                pass

            # Scroll to load reviews
            for _ in range(3):
                page.mouse.wheel(0, 2000)
                page.wait_for_timeout(1000)

            # Extract any review-like text
            selectors = [
                "div.ZmyHeo div div",
                "div.t-ZTKy div div",
                "div._6K-7Co",
                "div.col.EPCmJX div",
                "p._2-N8zT",
            ]
            for sel in selectors:
                elems = page.locator(sel).all()
                for el in elems:
                    try:
                        txt = (el.text_content() or "").replace("READ MORE", "").strip()
                        if 25 < len(txt) < 1500 and txt not in reviews:
                            reviews.append(txt)
                    except Exception:
                        continue
                if len(reviews) >= 5:
                    break

            # Open dedicated reviews page if too few
            if len(reviews) < 5:
                links = page.locator("a[href*='/product-reviews/']").all()
                if links:
                    href = links[0].get_attribute("href")
                    if href:
                        full = "https://www.flipkart.com" + href if href.startswith("/") else href
                        print(f"[Flipkart] Loading reviews page...")
                        page.goto(full, timeout=30000, wait_until="domcontentloaded")
                        page.wait_for_timeout(3000)
                        for _ in range(4):
                            page.mouse.wheel(0, 2000)
                            page.wait_for_timeout(800)
                        for sel in selectors:
                            for el in page.locator(sel).all():
                                try:
                                    txt = (el.text_content() or "").replace("READ MORE", "").strip()
                                    if 25 < len(txt) < 1500 and txt not in reviews:
                                        reviews.append(txt)
                                except Exception:
                                    continue

        except Exception as e:
            print(f"[Flipkart] Error: {e}")
        finally:
            browser.close()

    # Dedup
    reviews = list(dict.fromkeys(reviews))
    return product_name, reviews[:20]

"""
# ---------------- AMAZON (Playwright) ----------------
def extract_asin(url):
    patterns = [
        r"/dp/([A-Z0-9]{10})",
        r"/gp/product/([A-Z0-9]{10})",
        r"/product-reviews/([A-Z0-9]{10})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)

        if match:
            return match.group(1)

    return None
def scrape_amazon(url):
    reviews = []
    product_name = "Amazon Product"
    asin=extract_asin(url)
    if not asin:
        print("ASIN not fount")
        return product_name,[]
    review_url=f"https://www.amazon.in/product-reviews/{asin}"
    print("ASIN:",asin)
    print("Review URL:",review_url)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
          user_data_dir="amazon_profile",
          headless=False,
          viewport={"width":1366,"height":768},
          locale="en-IN"  
        )
        page = context.new_page()
        try:
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(2500)

            if "captcha" in page.content().lower():
                print("⚠️ Amazon CAPTCHA — try Flipkart URL instead.")
                context.close()
                return "Blocked by Amazon", []

            try:
                product_name = page.locator("#productTitle").first.text_content(timeout=3000).strip()
            except Exception:
                pass
            page.goto(review_url,timeout=60000)
            page.wait_for_timeout(5000)
            print("Current URL:",page.url)
            print("Page Title:",page.title())
            for _ in range(6):
                page.mouse.wheel(0, 3000)
                page.wait_for_timeout(1000)
            elements=page.locator("span[data-hook='review-body']").all()
            print("Review elements found:",len(elements))
            for el in elements:
                try:
                    txt=(el.text_content() or "").strip()
                    txt=(
                        txt.replace("Read more","")
                        .replace("...","")
                        .strip()
                    )
                    if len(txt)>15:
                        reviews.append(txt)
                except:
                    pass
           
        except Exception as e:
            print(f"[Amazon] Error: {e}")
        finally:
            context.close()

    return product_name, list(dict.fromkeys(reviews))[:20]

# ---------------- MAIN (used by app.py — same signature) ----------------
def scrape_reviews(url):
    try:
        site = detect_site(url)
        print(f"Detected site: {site}")

        #if site == "flipkart":
         #   name, reviews = scrape_flipkart(url)
        if site == "amazon":
            name, reviews = scrape_amazon(url)
        else:
            return "Unsupported site (use Flipkart or Amazon)", []

        print(f"✅ Got {len(reviews)} reviews for: {name}")
        return name, reviews
    except Exception as e:
        print("Scraping error:", e)
        return "Error", []

# Standalone test
if __name__ == "__main__":
    url = input("Paste product URL: ").strip()
    name, revs = scrape_reviews(url)
    print(f"\nProduct: {name}\nTotal reviews: {len(revs)}\n")
    for i, r in enumerate(revs[:5], 1):
        print(f"{i}. {r[:200]}\n")
