      window.addEventListener('DOMContentLoaded', () => {

          const themeSwitcher = document.querySelector('#bd-theme')
      
          if (!themeSwitcher) {
            return
          }
      
          document.querySelector('#bd-theme-text')
          document.querySelector(`[data-bs-theme-value="${theme}"]`)
      
          document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
            element.classList.remove('active')
            element.setAttribute('aria-pressed', 'false')
          })        
        })