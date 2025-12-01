package com.topai.incidenciasestacionamiento.controller;

import com.topai.incidenciasestacionamiento.dto.request.UsuarioRequestDTO;
import com.topai.incidenciasestacionamiento.dto.response.UsuarioResponseDTO;
import com.topai.incidenciasestacionamiento.service.UsuarioService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.security.Principal;

@RestController
@RequestMapping("/api/usuarios")
public class UsuarioController {

    @Autowired
    private UsuarioService usuarioService;

    @PostMapping("/registrar")
    public ResponseEntity<UsuarioResponseDTO> crearUsuario(@Valid @RequestBody UsuarioRequestDTO usuarioRequestDTO,
                                                           Principal principal){
        if (!usuarioRequestDTO.getCorreo().equals(principal.getName())){
            throw new RuntimeException("El correo no coincide");
        }

        return ResponseEntity.ok(usuarioService.registrarUsuario(usuarioRequestDTO));
    }

    @GetMapping("/perfil")
    public ResponseEntity<UsuarioResponseDTO> verMiPerfil(Principal principal){
        return ResponseEntity.ok(usuarioService.buscarPorCorreo(principal.getName()));
    }


}
