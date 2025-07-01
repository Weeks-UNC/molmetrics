import subprocess
from pathlib import Path
import filecmp

def test_molmetrics_integration(tmp_path):
    """
    Integration test for molmetrics.

    This test runs the molmetrics command with specific arguments and compares
    the generated output file with the expected results.
    """
    # Paths
    input_file = Path("/home/sethv/github/molmetrics/molmetrics/data/mini_test_library.sdf")
    expected_output_file = Path("/home/sethv/github/molmetrics/molmetrics/data/mini_test_library_output/mini_test_library_qed_reference.sdf")
    output_dir = tmp_path / "test_output"
    output_dir.mkdir()

    # Command to run
    command = [
        "python", "-m", "molmetrics",
        "-f", str(input_file),
        "-p", "-md", "-g",
        "-o", str(output_dir),
        "-s", "[#7]-[#6]-[#6]-[#6]-[#6]C#C", "[#6]C#C"
    ]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Assert the command ran successfully
    assert result.returncode == 0, f"Command failed with error: {result.stderr}"

    # Verify the output file exists
    generated_output_file = output_dir / "mini_test_library_qed.sdf"
    assert generated_output_file.exists(), "Output file was not generated."

    # Compare the generated output with the expected output
    if not filecmp.cmp(generated_output_file, expected_output_file, shallow=False):
        # Log differences for debugging
        with open(generated_output_file, "r") as gen_file:
            generated_content = gen_file.read()
        with open(expected_output_file, "r") as exp_file:
            expected_content = exp_file.read()
        
        print("\nGenerated Output:\n", generated_content)
        print("\nExpected Output:\n", expected_content)
        
        assert False, "Generated output file does not match the expected output."
