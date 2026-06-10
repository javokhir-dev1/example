import webview
import json
import os
from datetime import datetime

# Barcha so'rovlar saqlanadigan papkani yaratamiz
if not os.path.exists('sorovlar_logi'):
    os.makedirs('sorovlar_logi')

class TarmoqApi:
    def __init__(self, oyna_ref):
        self._oyna = oyna_ref

    def refresh_page(self):
        """Saytni qayta yuklash (refresh)"""
        if self._oyna:
            url = self._oyna.get_current_url()
            self._oyna.load_url(url)
            print(f"[*] Sahifa yangilandi: {url}")

    def log_request(self, data):
        """JavaScriptdan kelgan ma'lumotlarni (Request + Response) qabul qilib JSONga yozish"""
        fayl_nomi = "sorovlar_logi/barcha_sorovlar.json"
        
        # Mavjud ma'lumotlarni o'qib olamiz
        if os.path.exists(fayl_nomi):
            with open(fayl_nomi, 'r', encoding='utf-8') as f:
                try:
                    sorovlar = json.load(f)
                except json.JSONDecodeError:
                    sorovlar = []
        else:
            sorovlar = []
        
        # Yangi so'rovni qo'shamiz
        data['saqlangan_vaqt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sorovlar.append(data)
        
        # Hammasini bitta faylga yozamiz
        with open(fayl_nomi, 'w', encoding='utf-8') as f:
            json.dump(sorovlar, f, indent=4, ensure_ascii=False)
            
        print(f"[*] Saqlandi: {fayl_nomi} | Jami: {len(sorovlar)} ta | Status: {data.get('response_status')} | URL: {data.get('url')}")

def inyeksiya_qilish(oyna):
    """Oyna yuklanganda Request va Response'larni ushlovchi JS kodni saytga qo'shamiz"""
    js_kod = """
    (function() {
        // Keraksiz analitika/tracking domenlari ro'yxati
        const bloklangan_domenlar = [
            'mc.yandex.ru',
            'yandex.ru/metrika',
            'google-analytics.com',
            'googletagmanager.com',
            'analytics.google.com',
            'facebook.net',
            'connect.facebook.net',
            'doubleclick.net',
            'hotjar.com',
            'clarity.ms',
            'mixpanel.com',
            'segment.io',
            'segment.com',
            'amplitude.com',
            'sentry.io',
            'newrelic.com',
            'nr-data.net',
            'pixel.facebook.com',
            'bat.bing.com',
            'ads.linkedin.com',
            'snap.licdn.com',
            'tiktok.com/i18n',
            'analytics.tiktok.com',
            'criteo.com',
            'adservice.google.com'
        ];

        // URLni tekshirish funksiyasi
        function bloklangan_mi(url) {
            try {
                let tekshirish = url.toString().toLowerCase();
                return bloklangan_domenlar.some(d => tekshirish.includes(d));
            } catch(e) {
                return false;
            }
        }

        // 1. Fetch so'rovlari va javoblarini ushlash
        const originalFetch = window.fetch;
        window.fetch = async function(...args) {
            let url = args[0];
            let options = args[1] || {};
            let method = options.method || 'GET';
            let reqBody = options.body ? options.body.toString() : null;
            
            try {
                // Asl fetch so'rovini bajaramiz
                const response = await originalFetch.apply(this, args);
                
                // Bloklangan domenga so'rov bo'lsa — log qilmaymiz
                if (bloklangan_mi(url)) {
                    return response;
                }

                // Sayt buzilib qolmasligi uchun javobni nusxalaymiz (clone)
                const clonedResponse = response.clone();
                let resBody = "";
                
                try {
                    resBody = await clonedResponse.text();
                } catch (e) {
                    resBody = "Javobni o'qib bo'lmadi (ehtimol binar fayl yoki rasm)";
                }

                // Ma'lumotlarni Pythonga yuborish
                if (window.pywebview && window.pywebview.api) {
                    window.pywebview.api.log_request({
                        turi: 'fetch',
                        method: method,
                        url: url.toString(),
                        request_body: reqBody,
                        cookie: document.cookie,
                        vaqt: new Date().toISOString(),
                        response_status: response.status,
                        response_body: resBody
                    });
                }
                
                return response; // Saytga o'zining javobini qaytaramiz
            } catch (error) {
                console.error("Fetch xatosi ushlandi:", error);
                throw error;
            }
        };

        // 2. XMLHttpRequest (AJAX) so'rovlari va javoblarini ushlash
        const originalOpen = XMLHttpRequest.prototype.open;
        const originalSend = XMLHttpRequest.prototype.send;
        
        XMLHttpRequest.prototype.open = function(method, url) {
            this._method = method;
            this._url = url;
            return originalOpen.apply(this, arguments);
        };
        
        XMLHttpRequest.prototype.send = function(body) {
            let reqBody = body ? body.toString() : null;
            
            // Javob kelishini kutish (load hodisasi)
            this.addEventListener('load', function() {
                // Bloklangan domenga so'rov bo'lsa — log qilmaymiz
                if (bloklangan_mi(this._url)) return;

                if (window.pywebview && window.pywebview.api) {
                    window.pywebview.api.log_request({
                        turi: 'xhr',
                        method: this._method,
                        url: this._url,
                        request_body: reqBody,
                        cookie: document.cookie,
                        vaqt: new Date().toISOString(),
                        response_status: this.status,
                        response_body: this.responseText // Qaytib kelgan ma'lumot
                    });
                }
            });

            return originalSend.apply(this, arguments);
        };
    })();
    """
    oyna.evaluate_js(js_kod)

    # Refresh tugmasini qo'shish
    refresh_tugma_js = """
    (function() {
        if (document.getElementById('refresh-btn-pywebview')) return;

        var btn = document.createElement('button');
        btn.id = 'refresh-btn-pywebview';
        btn.innerHTML = '&#x21bb;';
        btn.title = 'Sahifani yangilash (Refresh)';
        btn.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 999999;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: none;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        `;

        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.15) rotate(90deg)';
            this.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.6)';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
            this.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
        });

        btn.addEventListener('click', function() {
            this.style.transform = 'scale(0.9) rotate(360deg)';
            setTimeout(function() {
                if (window.pywebview && window.pywebview.api) {
                    window.pywebview.api.refresh_page();
                } else {
                    location.reload();
                }
            }, 300);
        });

        document.body.appendChild(btn);
    })();
    """
    oyna.evaluate_js(refresh_tugma_js)

if __name__ == '__main__':
    # Avval API obyektini yaratamiz (oyna referensi keyinroq beriladi)
    api = TarmoqApi(None)

    # Oynani yaratamiz va js_api ni parametr sifatida beramiz
    oyna = webview.create_window(
        'Mening Dasturim', 
        'https://itv.uz/',
        js_api=api
    )

    # API ga oyna referensini beramiz
    api._oyna = oyna
    
    # Sayt yuklanganda JavaScript inyeksiyasini ishga tushirish
    oyna.events.loaded += lambda: inyeksiya_qilish(oyna)
    
    # Dasturni ishga tushirish
    webview.start()