import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# Import de votre nouvelle classe Page Object
from calculator_page import CalculatorPage

class TestCalculator:
    
    @pytest.fixture(scope="class")
    def driver(self):
        """Configuration du driver Chrome pour les tests"""
        chrome_options = Options()
        if os.getenv('CI'):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()


    def test_page_loads(self, driver):
        """Test 1: Vérifier que la page se charge correctement"""
        page = CalculatorPage(driver)
        page.load_page()
        
        # On vérifie le titre via le driver de l'objet page
        assert "Calculatrice Simple" in page.driver.title
        
        # Pour vérifier la présence, on peut utiliser le driver interne
        # (Ou idéalement ajouter une méthode is_displayed dans CalculatorPage)
        from selenium.webdriver.common.by import By
        assert page.driver.find_element(By.ID, "num1").is_displayed()
        assert page.driver.find_element(By.ID, "calculate").is_displayed()

    def test_addition(self, driver):
        """Test 2: Tester l'addition (Refactorisé 5.2)"""
        page = CalculatorPage(driver)
        page.load_page()
        
        page.enter_first_number("10")
        page.enter_second_number("5")
        page.select_operation("add")
        page.click_calculate()
        
        assert "Résultat: 15" in page.get_result()

    def test_division_by_zero(self, driver):
        """Test 3: Tester la division par zéro (Refactorisé 5.2)"""
        page = CalculatorPage(driver)
        page.load_page()
        
        page.enter_first_number("10")
        page.enter_second_number("0")
        page.select_operation("divide")
        page.click_calculate()
        
        assert "Erreur: Division par zéro" in page.get_result()

    def test_all_operations(self, driver):
        """Test 4: Tester toutes les opérations (Refactorisé 5.2)"""
        page = CalculatorPage(driver)
        page.load_page()
        
        operations = [
            ("add", "8", "2", "10"),
            ("subtract", "8", "2", "6"),
            ("multiply", "8", "2", "16"),
            ("divide", "8", "2", "4")
        ]
        
        for op, num1, num2, expected in operations:
            page.enter_first_number(num1) # La méthode nettoie le champ automatiquement
            page.enter_second_number(num2)
            page.select_operation(op)
            page.click_calculate()
            
            assert f"Résultat: {expected}" in page.get_result()

    def test_page_load_time(self, driver):
        """Test 5: Mesurer le temps de chargement (Performance)"""
        # On utilise le chargement manuel pour capter le temps exact
        # mais on peut utiliser page.load_page() si on ne mesure pas le chargement du fichier lui-même
        page = CalculatorPage(driver)
        
        start_time = time.time()
        page.load_page()
        
        # On attend qu'un élément clé soit présent pour arrêter le chrono
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "calculator"))
        )
        
        load_time = time.time() - start_time
        print(f"Temps de chargement: {load_time:.2f} secondes")
        assert load_time < 3.0

    # --- Tests ajoutés à l'exercice 5.1 (Maintenant refactorisés) ---

    def test_decimals(self, driver):
        """Test 5.1.A: Tester avec des nombres décimaux"""
        page = CalculatorPage(driver)
        page.load_page()
        
        page.enter_first_number("5.5")
        page.enter_second_number("2.2")
        page.select_operation("add")
        page.click_calculate()
        
        assert "Résultat: 7.7" in page.get_result()

    def test_negative_numbers(self, driver):
        """Test 5.1.B: Tester avec des nombres négatifs"""
        page = CalculatorPage(driver)
        page.load_page()
        
        page.enter_first_number("-10")
        page.enter_second_number("-5")
        page.select_operation("multiply")
        page.click_calculate()
        
        assert "Résultat: 50" in page.get_result()

    def test_ui_appearance(self, driver):
        """Test 5.1.C: Interface Utilisateur"""
        page = CalculatorPage(driver)
        page.load_page()
        
        # Note: Le Page Object du TP n'a pas de méthodes CSS spécifiques.
        # On accède donc au driver via l'objet page pour ces assertions spécifiques.
        from selenium.webdriver.common.by import By
        
        container = page.driver.find_element(By.CLASS_NAME, "container")
        width = container.value_of_css_property("max-width")
        assert width == "400px"
        
        result_box = page.driver.find_element(By.ID, "result")
        bg_color = result_box.value_of_css_property("background-color")
        assert "240, 240, 240" in bg_color

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])