package com.topai.incidenciasestacionamiento.dto.request;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class LoginRequestDTO {
    @NotBlank
    private String correo;
    @NotBlank
    private String password;
}
