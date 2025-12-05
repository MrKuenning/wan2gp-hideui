import gradio as gr
from shared.utils.plugins import WAN2GPPlugin

PlugIn_Name = "Mobile Toggle Helper"
PlugIn_Id = "MobileToggleHelper"

class MobileTogglePlugin(WAN2GPPlugin):
    def __init__(self):
        super().__init__()
        self.name = PlugIn_Name
        self.version = "3.1"
        self.description = "Floating menu. Safe blank-space removal using State Tags."

    def setup_ui(self):
        self.add_custom_js(self.inject_floating_buttons_js())

    def inject_floating_buttons_js(self) -> str:
        return r"""
        (function(){
            // CONFIGURATION: Your custom list with defaults
            const TARGETS = [
                // Hide the Title 
                { id: "header", labels: ["deepbeepmeep"], name: "Header", default: false },
                // Hide the Model Selection 
                { id: "model_selection", labels: ["dropdown dropdown"], name: "Model Selector", default: true },
                // Hide the Model Information 
                { id: "model_info", labels: ["Attention Mode"], name: "Model Info", default: false },
                // Hide the Image input Options 
                { id: "image_input", labels: ["location start vide", "end image"], name: "Input Options", default: true },
                // Hide the Prompt Image Options 
                { id: "video_to_video", labels: ["video to video"], name: "Text Image Options", default: true },
                // Hide both the Enhance Prompt Button and Dropdown
                { id: "enhance_prompt", labels: ["enhance prompt","enhance prompt using"], name: "Enhance Prompt", default: true },
                // Hide both Resolution Catagory and Selector
                { id: "res_group", labels: ["resolution", "category"], name: "Resolution Options", default: true },
                // Hide Number of Frames Slider
                { id: "frames", labels: ["number of frames"], name: "Number of Frames", default: true },
                // Hide Inference Steps Slider
                { id: "inf_steps", labels: ["number of inference steps"], name: "Inference Steps", default: false },
                // Hide All three settings Buttons                
                { id: "settings_buttons", labels: ["set settings as default", "Export settings to file", "reset settings"], name: "Settings Buttons", default: false },
                // Hide Load from File Drop Box
                { id: "load_vid", labels: ["load settings from video"], name: "Load from Video", default: true },
                // Hide Download Lora from URL  
                { id: "lora", labels: ["download lora", "lora url"], name: "Download LoRA", default: false },
                // Hide Video Info  
                { id: "video_info", labels: ["video info"], name: "Video Info", default: true }
            ];

            // --- SAFETY LOGIC START ---

            function isElementVisible(el) {
                return el.style.display !== "none";
            }

            // Hides an element and safely collapses empty parents
            function safeHide(element) {
                element.style.display = "none";
                
                let current = element.parentElement;
                let safetyCounter = 0;

                // Walk up the tree to hide empty wrappers
                while (current && safetyCounter < 5) {
                    if (current.tagName === "BODY" || current.classList.contains("gradio-container") || current.id === "root") break;

                    // Get immediate children that are usually layout elements
                    const children = Array.from(current.children).filter(c => 
                        ["DIV", "BUTTON", "SPAN", "INPUT", "LABEL", "FORM", "FIELDSET"].includes(c.tagName)
                    );

                    // If ALL relevant children are hidden, we can hide this parent
                    const allHidden = children.every(c => c.style.display === "none");

                    if (allHidden && children.length > 0) {
                        // TAG IT so we know WE hid it, not Gradio
                        current.dataset.pluginHidden = "true"; 
                        current.style.display = "none";
                        current = current.parentElement;
                        safetyCounter++;
                    } else {
                        // Parent still has visible stuff, stop walking up
                        break;
                    }
                }
            }

            // Shows an element and ONLY restores parents that WE hid
            function safeShow(element) {
                element.style.display = ""; // Remove inline display:none

                let current = element.parentElement;
                let safetyCounter = 0;

                while (current && safetyCounter < 5) {
                    if (current.tagName === "BODY") break;

                    // CHECK THE TAG: Only unhide if we hid it previously
                    if (current.dataset.pluginHidden === "true") {
                        current.style.display = ""; 
                        delete current.dataset.pluginHidden; // Clean up tag
                        current = current.parentElement;
                        safetyCounter++;
                    } else {
                        // If it wasn't hidden by us, leave it alone (Gradio might want it hidden)
                        break;
                    }
                }
            }

            // --- SAFETY LOGIC END ---

            function setVisibility(searchLabels, shouldShow) {
                const terms = Array.isArray(searchLabels) ? searchLabels : [searchLabels];
                
                // Find all components
                const allElements = Array.from(document.querySelectorAll("div[id^='component-'], button[id^='component-']"));

                terms.forEach(term => {
                    const lbl = term.toLowerCase().trim();

                    const candidates = allElements.filter(el => {
                        const text = (el.innerText || el.textContent || "").replace(/\s+/g,' ').trim().toLowerCase();
                        return text.includes(lbl);
                    });

                    // Filter for deepest match
                    const targets = candidates.filter(el => {
                        const containsChildMatch = candidates.some(other => other !== el && el.contains(other));
                        return !containsChildMatch;
                    });

                    targets.forEach(el => {
                        if (shouldShow) {
                            safeShow(el);
                        } else {
                            safeHide(el);
                        }
                    });
                });
            }

            function createUI() {
                if (document.getElementById("floating-toggle-container")) return;

                const container = document.createElement("div");
                container.id = "floating-toggle-container";
                Object.assign(container.style, {
                    position: "fixed", bottom: "16px", right: "16px", zIndex: "999999",
                    display: "flex", flexDirection: "column", alignItems: "flex-end", gap: "10px"
                });

                const menu = document.createElement("div");
                menu.id = "floating-menu";
                Object.assign(menu.style, {
                    background: "rgba(30, 30, 30, 0.95)", border: "1px solid #444", borderRadius: "8px",
                    padding: "10px", display: "none", flexDirection: "column", gap: "8px",
                    minWidth: "200px", boxShadow: "0 4px 12px rgba(0,0,0,0.5)", color: "white",
                    maxHeight: "60vh", overflowY: "auto"
                });

                const createCheckbox = (labelText, onChange, isChecked=true) => {
                    const label = document.createElement("label");
                    Object.assign(label.style, { display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "14px" });
                    
                    const input = document.createElement("input");
                    input.type = "checkbox";
                    input.checked = isChecked;
                    input.style.cursor = "pointer";
                    input.onchange = (e) => onChange(e.target.checked);
                    
                    const span = document.createElement("span");
                    span.textContent = labelText;
                    
                    label.appendChild(input);
                    label.appendChild(span);
                    return { label, input };
                };

                const toggleAllRow = createCheckbox("Show/Hide All", (checked) => {
                    TARGETS.forEach(target => {
                        const cb = document.getElementById(`cb-${target.id}`);
                        if(cb) {
                            cb.checked = checked;
                            setVisibility(target.labels, checked);
                        }
                    });
                }, true);
                
                toggleAllRow.label.style.fontWeight = "bold";
                toggleAllRow.label.style.borderBottom = "1px solid #555";
                toggleAllRow.label.style.paddingBottom = "8px";
                menu.appendChild(toggleAllRow.label);

                TARGETS.forEach(target => {
                    const initialStatus = (target.default !== undefined) ? target.default : true;
                    const row = createCheckbox(target.name, (checked) => {
                        setVisibility(target.labels, checked);
                    }, initialStatus);
                    row.input.id = `cb-${target.id}`;
                    menu.appendChild(row.label);
                    
                    // Init
                    setVisibility(target.labels, initialStatus);
                });

                const mainBtn = document.createElement("button");
                mainBtn.textContent = "☰ UI";
                Object.assign(mainBtn.style, {
                    padding: "10px 16px", borderRadius: "24px",
                    background: "#0284c7", color: "white", border: "none", cursor: "pointer",
                    boxShadow: "0 2px 8px rgba(0,0,0,0.4)", fontWeight: "bold"
                });

                mainBtn.onclick = () => {
                    const isHidden = menu.style.display === "none";
                    menu.style.display = isHidden ? "flex" : "none";
                    mainBtn.textContent = isHidden ? "✕ Close" : "☰ UI";
                };

                container.appendChild(menu);
                container.appendChild(mainBtn);
                document.body.appendChild(container);
            }

            function init() { createUI(); }

            window.addEventListener("gradioLoaded", () => setTimeout(init, 300));
            document.addEventListener("DOMContentLoaded", () => setTimeout(init, 500));
            window.addEventListener("load", () => setTimeout(init, 700));

            let tries = 0;
            const interval = setInterval(() => {
                tries++;
                init();
                if (tries > 10) clearInterval(interval);
            }, 800);
            
            setTimeout(init, 100);
        })();
        """