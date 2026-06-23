import React, { createContext, useContext, useState } from "react";
import translations from "../i18n/translations";

const LanguageContext = createContext(null);

export function LanguageProvider({ children }) {
  const [lang, setLangState] = useState(
    () => localStorage.getItem("onboardai_lang") || "en"
  );

  const setLang = (l) => {
    localStorage.setItem("onboardai_lang", l);
    setLangState(l);
  };

  const t = (key, vars = {}) => {
    const keys = key.split(".");
    let val = translations[lang];
    for (const k of keys) {
      val = val?.[k];
      if (val === undefined) return key;
    }
    if (typeof val !== "string") return key;
    return Object.entries(vars).reduce(
      (s, [k, v]) => s.replaceAll(`{${k}}`, v),
      val
    );
  };

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}
