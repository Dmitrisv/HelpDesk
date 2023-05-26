    (() => {
        'use strict'     
          const themeSwitcher = document.querySelector('#bd-theme')
      
          if (!themeSwitcher) {
            return
          }
      
          const themeSwitcherText = document.querySelector('#bd-theme-text')
          const activeThemeIcon = document.querySelector('.theme-icon-active use')
          const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`)
          const svgOfActiveBtn = btnToActive.querySelector('svg use').getAttribute('href')
      
          document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
            element.classList.remove('active')
            element.setAttribute('aria-pressed', 'false')
          })
      
          btnToActive.classList.add('active')
          btnToActive.setAttribute('aria-pressed', 'true')
          activeThemeIcon.setAttribute('href', svgOfActiveBtn)
          const themeSwitcherLabel = `${themeSwitcherText.textContent} (${btnToActive.dataset.bsThemeValue})`
          themeSwitcher.setAttribute('aria-label', themeSwitcherLabel)
      
          if (focus) {
            themeSwitcher.focus()
          }
      

      })()