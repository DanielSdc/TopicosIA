package com.topai.incidenciasestacionamiento.controller;

import com.topai.incidenciasestacionamiento.dto.request.IncidenciaRequestDTO;
import com.topai.incidenciasestacionamiento.dto.response.IncidenciaResponseDTO;
import com.topai.incidenciasestacionamiento.service.IncidenciaService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.security.Principal;
import java.util.List;

@RestController
@RequestMapping("/api/incidencias")
public class IncidenciaController {

    @Autowired
    private IncidenciaService incidenciaService;

    @PostMapping
    public ResponseEntity<IncidenciaResponseDTO> crearIncidencia (@Valid @RequestBody IncidenciaRequestDTO incidenciaRequestDTO,
                                                                  Principal principal){

        if (principal == null){
            throw new RuntimeException("Usuario no identificado");
        }
        return ResponseEntity.ok(incidenciaService.crearIncidencia(incidenciaRequestDTO, principal.getName()));
    }

    @GetMapping("/recibidas")
    public ResponseEntity<List<IncidenciaResponseDTO>> incidenciasRecibidas (Principal principal){
        return ResponseEntity.ok(incidenciaService.traerIncidenciasDelUsuario(principal.getName()));
    }

    @GetMapping("/enviadas")
    public ResponseEntity<List<IncidenciaResponseDTO>> incidenciasEnviadas (Principal principal){
        return ResponseEntity.ok(incidenciaService.traerIncidenciasCreadasPorUsuario(principal.getName()));
    }

}
