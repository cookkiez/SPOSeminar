import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;

public class Sandbox {
	public static void main(String[] args) throws MalformedURLException, IOException {
		System.setSecurityManager(new SecurityManager());
		SecurityManager mng = System.getSecurityManager();
		System.out.println(mng);
		new URL("http://www.google.com").openConnection().connect();
		System.out.println("Povezano!");
	}
}
