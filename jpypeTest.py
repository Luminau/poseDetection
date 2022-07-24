# Import module
import jpype
import java.lang

jpype.startJVM(classpath =['naturalmouse-2.0.3.jar'])

jpype.java.lang.System.out.println("hello")
import com.github.joonasvali.naturalmouse
MouseMotionFactory.getDefault()