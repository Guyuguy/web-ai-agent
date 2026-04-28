import os, json, re, yaml, hashlib, sys, argparse
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from DrissionPage import ChromiumPage, ChromiumOptions
from dotenv import load_dotenv
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

os.environ['NO_PROXY'] = '127.0.0.1,localhost'
os.environ['no_proxy'] = '127.0.0.1,localhost'

client = OpenAI(api_key=os.getenv("GLM_TOKEN"), base_url=os.getenv("GLM_BASE_URL"))
MODEL = os.getenv("GLM_MODEL", "glm-4.7")
SKILL_DIR = Path(os.getenv("SKILL_DIR", "./skills"))

EXTRACT_JS = """
var els = document.querySelectorAll('button, a, input, select, textarea');
var data = [];
for (var i = 0; i < Math.min(els.length, 50); i++) {
    var el = els[i];
    var selector = el.id ? '#' + el.id : (el.className ? '.' + el.className.split(' ')[0] : el.tagName.toLowerCase());
    data.push({
        tag: el.tagName.toLowerCase(),
        text: (el.innerText || el.getAttribute('placeholder') || '').trim().substring(0, 50),
        selector: selector,
        type: el.getAttribute('type') || ''
    });
}
return data;"""

def learn_page(url: str):
    """模式1：学习网页，生成技能"""
    # 创建临时用户数据目录，确保每次都打开新窗口
    temp_dir = tempfile.mkdtemp(prefix="web_agent_")
    page = None

    try:
        # 配置浏览器选项
        co = ChromiumOptions()
        co.set_argument('--user-data-dir', temp_dir)
        co.set_argument('--no-first-run')
        co.set_argument('--no-default-browser-check')
        co.set_argument('--disable-session-crashed-bubble')
        co.set_argument('--disable-infobars')
        co.set_argument('--proxy-server=http://109.2.0.41:9090')
        co.set_argument('--proxy-bypass-list=<-loopback>')
        co.set_argument('--ignore-certificate-errors')

        # 创建新的浏览器页面（每次都是新窗口）
        page = ChromiumPage(co)
        new_tab = page.new_tab()
        new_tab.get(url)
        new_tab.wait.doc_loaded(5)

        els = new_tab.run_js(EXTRACT_JS)

        if not els:
            print("[WARNING] 未提取到页面元素，请检查网页是否正常加载")
            return

        page_id = hashlib.md5(url.encode()).hexdigest()[:8]
        save_path = SKILL_DIR / page_id
        save_path.mkdir(parents=True, exist_ok=True)

        elements_data = {
            "url": url, "title": new_tab.title, "snapshot_at": datetime.now().isoformat(), "elements": els
        }

        with open(save_path / "elements.json", 'w', encoding='utf-8') as f:
            json.dump(elements_data, f, ensure_ascii=False, indent=2)

        print(f"[INFO] 页面元素已提取，ID: {page_id}")

        # AI 生成技能
        prompt = f"""分析以下网页元素，生成 3 个高频操作技能。

网页元素：
{json.dumps(els[:10], ensure_ascii=False, indent=2)}

要求：只返回JSON数组，每个技能包含skill_id, intent_keywords, description, steps。
示例：
[{{"skill_id":"search","intent_keywords":["搜索","search"],"description":"搜索","steps":[{{"action":"input","target_selector":"#kw","value":"{{text}}"}},{{"action":"click","target_selector":"#su"}}]}}]"""

        resp = client.chat.completions.create(model=MODEL, messages=[{"role":"user","content":prompt}])
        raw = resp.choices[0].message.content
        print(f"[DEBUG] AI 返回内容: {raw[:500]}")
        json_str = re.search(r'\[.*\]', raw, re.DOTALL)
        if not json_str:
            print(f"[ERROR] 未能从 AI 返回中提取 JSON")
            return
        skills = json.loads(json_str.group())

        with open(save_path / "skills.yaml", 'w', encoding='utf-8') as f:
            yaml.dump({"skills": skills}, f, allow_unicode=True)

        print(f"[SUCCESS] AI 已生成 {len(skills)} 个技能，保存至: {save_path}")

    except Exception as e:
        print(f"[ERROR] 学习失败: {e}")
    finally:
        if page:
            page.quit()
        # 清理临时目录
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"[INFO] 已清理临时目录: {temp_dir}")
        except Exception as e:
            print(f"[WARNING] 清理临时目录失败: {e}")

def run_skill(page_id: str, intent: str):
    """模式2：执行技能"""
    skill_file = SKILL_DIR / page_id / "skills.yaml"
    if not skill_file.exists():
        print("[ERROR] 未找到技能文件，请先运行 learn 模式")
        return

    with open(skill_file, 'r', encoding='utf-8') as f:
        skills = yaml.safe_load(f)["skills"]

    intent_lower = intent.lower()
    matched = None
    for s in skills:
        if any(k.lower() in intent_lower for k in s.get("intent_keywords", [])):
            matched = s; break

    if not matched:
        print("[WARNING] 未匹配到技能。可用意图:", [s["intent_keywords"] for s in skills])
        return

    # 创建临时用户数据目录，确保每次都打开新窗口
    temp_dir = tempfile.mkdtemp(prefix="web_agent_run_")

    try:
        # 配置浏览器选项
        co = ChromiumOptions()
        co.set_argument('--user-data-dir', temp_dir)
        co.set_argument('--no-first-run')
        co.set_argument('--no-default-browser-check')
        co.set_argument('--disable-session-crashed-bubble')
        co.set_argument('--disable-infobars')
        co.set_argument('--proxy-server=http://109.2.0.41:9090')
        co.set_argument('--proxy-bypass-list=<-loopback>')
        co.set_argument('--ignore-certificate-errors')

        # 创建新的浏览器页面（每次都是新窗口）
        page = ChromiumPage(co)
        new_tab = page.new_tab()
        print(f"[INFO] 匹配到技能: {matched['description']}")
        print(f"[INFO] 正在打开新窗口执行技能...")

        with open(SKILL_DIR / page_id / "elements.json", 'r', encoding='utf-8') as f:
            url = json.load(f)["url"]
        new_tab.get(url)
        new_tab.wait.doc_loaded(2)

        for step in matched["steps"]:
            sel = step["target_selector"]
            el = new_tab.ele(sel, timeout=5)
            if not el:
                print(f"[ERROR] 元素未找到: {sel}"); continue
            act = step["action"]
            if act == "input":
                val = step.get("value", "")
                for k, v in {"username":"test", "password":"123456", "search_text":"AI"}.items():
                    val = val.replace(f"{{{k}}}", v)
                el.input(val, clear=True)
            elif act == "click":
                try:
                    el.click()
                except Exception as e:
                    print(f"[WARNING] 点击失败: {e}, 尝试使用 JavaScript 点击")
                    new_tab.run_js(f"document.querySelector('{sel}').click()")
            elif act == "wait": new_tab.wait.load_start(float(step.get("seconds", 1)))
            print(f"  [SUCCESS] 执行: {act} -> {sel}")

        print(f"[INFO] 任务执行完成，浏览器保持打开状态")
        print(f"[INFO] 临时用户数据目录: {temp_dir}")
        print(f"[INFO] 如需关闭浏览器，请手动关闭浏览器窗口")

        # 不关闭浏览器，保持打开状态
        # page.quit()

    finally:
        # 不清理临时目录，因为浏览器还在使用
        # 用户需要手动关闭浏览器后，临时目录才会被清理
        print(f"[INFO] 浏览器保持运行中，不关闭浏览器和临时目录")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI网页自动化技能引擎")
    parser.add_argument("mode", choices=["learn", "run"], help="learn: 学习网页 | run: 执行技能")
    parser.add_argument("--url", help="学习时的网页地址")
    parser.add_argument("--page_id", help="执行时的页面ID（learn后终端会打印）")
    parser.add_argument("--intent", help="执行时的自然语言指令")
    args = parser.parse_args()

    if args.mode == "learn":
        if not args.url: print("[ERROR] learn 模式需指定 --url"); sys.exit(1)
        learn_page(args.url)
    else:
        if not args.page_id or not args.intent:
            print("[ERROR] run 模式需指定 --page_id 和 --intent"); sys.exit(1)
        run_skill(args.page_id, args.intent)
