import unittest
import sys
import os
import json
from datetime import datetime
from backend_app.tests.test_malware_analysis import TestMalwareAnalysis
from backend_app.tests.test_integration import TestIntegration
from backend_app.tests.test_system import TestSystem

def run_tests():
    """Run all tests and generate a report"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMalwareAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestSystem))
    
    # Create test runner with custom result class
    class TestResult(unittest.TestResult):
        def __init__(self):
            super().__init__()
            self.results = []
        
        def addSuccess(self, test):
            super().addSuccess(test)
            self.results.append({
                'test': str(test),
                'status': 'success',
                'error': None
            })
        
        def addError(self, test, err):
            super().addError(test, err)
            self.results.append({
                'test': str(test),
                'status': 'error',
                'error': str(err[1])
            })
        
        def addFailure(self, test, err):
            super().addFailure(test, err)
            self.results.append({
                'test': str(test),
                'status': 'failure',
                'error': str(err[1])
            })
    
    # Run tests
    result = TestResult()
    suite.run(result)
    
    # Generate report
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_tests': result.testsRun,
        'successes': len([r for r in result.results if r['status'] == 'success']),
        'failures': len([r for r in result.results if r['status'] == 'failure']),
        'errors': len([r for r in result.results if r['status'] == 'error']),
        'test_results': result.results
    }
    
    # Save report
    report_dir = os.path.join(os.path.dirname(__file__), 'test_reports')
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    report_file = os.path.join(report_dir, f'test_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=4)
    
    # Print summary
    print("\nTest Summary:")
    print(f"Total Tests: {report['total_tests']}")
    print(f"Successes: {report['successes']}")
    print(f"Failures: {report['failures']}")
    print(f"Errors: {report['errors']}")
    print(f"\nDetailed report saved to: {report_file}")
    
    # Return appropriate exit code
    return 0 if report['failures'] == 0 and report['errors'] == 0 else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 